"""Responsive images: dimensions, the print mat, WebP, and click-through.

The Markdown image hook emits width and height, a srcset of derivatives, and
a WebP <picture> when the format earns it. Every article image wears the
print mat. The wrapper is a link when the original is wider than the content
column, the page asks for linkOriginals, or the file on the page is a
lighter re-encode of a heavy master. The href is the committed original.
"""

import os
import re
from html.parser import HTMLParser
from pathlib import Path
from unittest import TestCase

from helpers import ROOT, css_bundle, read, walk_html
from test_headers import matcher, raw_rules


COLUMN = 750
MAX_WIDTH = 1500
LADDER = (480, 750, 1125)
HEAVY_BYTES = 500_000
IMMUTABLE = ["public, max-age=31536000, immutable"]

# Originals wider than this are served as a downscale. The figure is the
# original's pixel width, read back out of the "view full size (W×H)" label.
FULL_SIZE = re.compile(r"view full size \((\d+)×(\d+)\)")
SRCSET_WIDTH = re.compile(r"\s(\d+)w$")


def classes(attrs):
    return (attrs.get("class") or "").split()


def expected_widths(source_width):
    cap = min(source_width, MAX_WIDTH)
    widths = [w for w in LADDER if w * 100 < cap * 85]
    widths.append(cap)
    return widths


def srcset_widths(value):
    return [int(SRCSET_WIDTH.search(part).group(1)) for part in value.split(",")]


def mat_kind(ancestors):
    """The print-mat wrapper, looking through a <picture>."""
    for tag, attrs in reversed(ancestors):
        if tag == "picture":
            continue
        kind = classes(attrs)
        if tag == "a" and "img-full" in kind:
            return "full"
        if tag == "span" and "img-mat" in kind:
            return "mat"
        return None
    return None


def full_anchor(ancestors):
    for tag, attrs in reversed(ancestors):
        if tag == "a" and "img-full" in classes(attrs):
            return attrs
    return None


def original_urls():
    """Page-bundle images, keyed by the URL Hugo publishes for the original.

    The published directory is the front-matter slug when the bundle sets
    one, not the folder the file sits in.
    """
    urls = {}
    content = ROOT / "content"
    for path in content.rglob("*"):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".gif"}:
            continue
        if path.name.startswith("."):
            continue
        bundle = path.parent
        index = bundle / "index.md"
        if not index.is_file():
            continue
        slug = None
        for line in index.read_text(encoding="utf-8").splitlines():
            if line.startswith(("---", "+++")):
                break
            match = re.match(r'^slug:\s*"?([^"\n]+)"?\s*$', line)
            if match:
                slug = match.group(1)
                break
        section = bundle.parent.relative_to(content).as_posix()
        if section == ".":
            section = ""
        name = f"{slug}/{path.name}" if slug else path.relative_to(bundle.parent).as_posix()
        url = "/" + "/".join(part for part in (section, name) if part)
        urls[url] = path
    return urls


class ImageParents(HTMLParser):
    """Every <img>, its open ancestors, and any <source> in its <picture>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.images = []
        self.sources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "source":
            self.sources.append(attrs)
            return
        if tag == "picture":
            self.sources = []
        if tag == "img":
            sources = list(self.sources) if any(t == "picture" for t, _ in self.stack) else []
            self.images.append((attrs, list(self.stack), sources))
            return
        self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == "picture":
            self.sources = []
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def images_in(html):
    parser = ImageParents()
    parser.feed(html)
    return parser.images


def articles():
    for path in walk_html():
        rel = "/" + path.relative_to(ROOT / "public").as_posix()
        if not re.fullmatch(r"/(?:notes/)?\d{4}/[^/]+/index.html", rel):
            continue
        yield rel[: -len("index.html")], images_in(read(rel))


class TestImages(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.originals = original_urls()

    def test_every_image_declares_its_size(self):
        """An image with no dimensions cannot reserve its box, so the page
        jumps when it arrives. The hook knows local images' real size."""
        missing = []
        for path in walk_html():
            rel = "/" + path.relative_to(ROOT / "public").as_posix()
            for img, _, _ in images_in(read(rel)):
                src = img.get("src", "")
                if src.startswith(("http://", "https://", "//", "data:")):
                    continue
                if not img.get("width") or not img.get("height"):
                    missing.append(f"{rel} -> {src}")
        self.assertEqual(missing, [])

    def test_home_avatar_is_small_and_high_priority(self):
        images = images_in(read("/index.html"))
        self.assertEqual(len(images), 1)
        avatar = images[0][0]
        self.assertEqual(avatar["loading"], "eager")
        self.assertEqual(avatar["fetchpriority"], "high")
        self.assertIn("390w", avatar["srcset"])
        src = ROOT / "public" / avatar["src"].lstrip("/")
        self.assertLess(src.stat().st_size, 40000)

    def test_article_images_are_matted_and_only_some_are_links(self):
        """The mat wraps the picture, or the img when there is no picture.
        A link carries an accessible name; a plain mat is not a link."""
        seen = 0
        for url, images in articles():
            for img, ancestors, sources in images:
                seen += 1
                kind = mat_kind(ancestors)
                self.assertIn(kind, ("full", "mat"), url)
                if sources:
                    self.assertEqual(ancestors[-1][0], "picture", url)
                anchor = full_anchor(ancestors)
                if kind == "full":
                    self.assertIsNotNone(anchor, url)
                    self.assertIn("view full size", anchor.get("aria-label", ""), url)
                    self.assertNotIn("_hu_", anchor["href"], url)
                else:
                    self.assertIsNone(anchor, url)
                    self.assertNotIn("<a", img.get("src", ""))
        self.assertGreater(seen, 100)

    def test_originals_wider_than_the_column_link(self):
        """750px is the column. 1500px is only the srcset cap, so a 1024px
        file still links. A 500px file and a GIF do not. The journal photo
        links to the committed original, not its hashed display file."""
        goodbye, _ = next(item for item in articles() if item[0].startswith("/2012/saying-goodbye"))
        resized = [
            (img, ancestors)
            for img, ancestors, _ in goodbye
            if (anchor := full_anchor(ancestors)) and anchor.get("href") != img.get("src")
        ]
        self.assertTrue(resized)
        for img, ancestors in resized:
            label = full_anchor(ancestors)["aria-label"]
            self.assertGreater(int(FULL_SIZE.search(label).group(1)), MAX_WIDTH)

        grim = images_in(read("/2012/a-developers-conundrum-dev-prod-parity/index.html"))
        self.assertEqual(len(grim), 1)
        self.assertEqual(mat_kind(grim[0][1]), "full")
        href = full_anchor(grim[0][1])["href"]
        self.assertIn("grim-reaper-writing-sketch", href)
        self.assertNotIn("_hu_", href)

        journal = images_in(read("/2022/journaling-the-best-habit-i-picked-up-in-2021/index.html"))
        photo = next(item for item in journal if "my-journal" in item[0]["src"])
        self.assertEqual(mat_kind(photo[1]), "full")
        href = full_anchor(photo[1])["href"]
        self.assertTrue(href.endswith("/my-journal.jpg"), href)
        self.assertNotIn("_hu_", href)

        luffy = images_in(read("/2013/5-am/index.html"))
        sketch = next(item for item in luffy if item[0]["src"].endswith("/luffy-sketch.jpg"))
        self.assertEqual(mat_kind(sketch[1]), "mat")
        self.assertIsNone(full_anchor(sketch[1]))

        graphql = images_in(read("/2020/rest-api-design/index.html"))
        gif = next(item for item in graphql if item[0]["src"].endswith("/rest-to-graphql.gif"))
        self.assertEqual(mat_kind(gif[1]), "mat")
        self.assertTrue(any(mat_kind(ancestors) == "full" for _, ancestors, _ in graphql))

    def test_the_mat_does_not_wrap_the_avatar(self):
        for path in walk_html():
            rel = "/" + path.relative_to(ROOT / "public").as_posix()
            if re.fullmatch(r"/(?:notes/)?\d{4}/[^/]+/index.html", rel) or rel == "/about/index.html":
                continue
            for _, ancestors, _ in images_in(read(rel)):
                self.assertIsNone(mat_kind(ancestors), rel)

    def test_stylesheet_carries_the_mat_and_expand_mark(self):
        css = css_bundle()
        for needle in ("img-mat", "zoom-in", "fit-content", "#d0d0d0", "focus-visible"):
            self.assertIn(needle, css)
        self.assertTrue("M9.5 2.5" in css or "M9.5%202.5" in css)
        self.assertNotIn("a.img-full:focus-visible{outline:none", css)
        self.assertNotIn("a.img-full:focus-visible{outline:0", css)
        self.assertIn("a.img-full picture", css)
        self.assertIn("img-mat picture", css)

    def test_article_images_keep_loading_and_dimensions(self):
        for url, images in articles():
            for index, (img, _, _) in enumerate(images):
                src = img.get("src", "")
                if src.startswith(("http://", "https://", "//")):
                    continue
                if index == 0:
                    self.assertEqual(img.get("loading"), "eager", f"{url} {src}")
                    self.assertEqual(img.get("fetchpriority"), "high", f"{url} {src}")
                else:
                    self.assertEqual(img.get("loading"), "lazy", f"{url} {src}")
                    self.assertNotIn("fetchpriority", img, f"{url} {src}")
                self.assertEqual(img.get("decoding"), "async", f"{url} {src}")
                if not src.endswith(".gif"):
                    self.assertLessEqual(int(img["width"]), MAX_WIDTH, f"{url} {src}")

    def test_candidates_follow_the_ladder(self):
        checked = 0
        for url, images in articles():
            for img, ancestors, _ in images:
                src = img.get("src", "")
                if src.endswith(".gif") or src.startswith(("http://", "https://", "//")):
                    continue
                anchor = full_anchor(ancestors)
                if anchor and (match := FULL_SIZE.search(anchor.get("aria-label", ""))):
                    source_width = int(match.group(1))
                    source_height = int(match.group(2))
                else:
                    source_width = int(img["width"])
                    source_height = int(img["height"])
                widths = expected_widths(source_width)
                if len(widths) == 1:
                    self.assertNotIn("srcset", img, f"{url} {src}")
                else:
                    self.assertEqual(srcset_widths(img["srcset"]), widths, f"{url} {src}")
                    self.assertIn("sizes", img, f"{url} {src}")
                self.assertEqual(int(img["width"]), widths[-1], f"{url} {src}")
                self.assertLessEqual(int(img["width"]), source_width, f"{url} {src}")
                expect_h = round(source_height * int(img["width"]) / source_width)
                self.assertAlmostEqual(int(img["height"]), expect_h, delta=1, msg=f"{url} {src}")
                checked += 1
        self.assertGreater(checked, 100)

    def test_photos_offer_webp_and_the_img_stays_a_real_image(self):
        checked = 0
        for url, images in articles():
            for img, ancestors, sources in images:
                src = img.get("src", "")
                if src.endswith(".gif") or src.startswith(("http://", "https://", "//")):
                    self.assertEqual(sources, [], f"{url} {src}")
                    continue
                self.assertNotIn("avif", " ".join(source.get("type", "") for source in sources))
                path = src.split("?", 1)[0].split("#", 1)[0]
                self.assertIn(Path(path).suffix.lower(), {".jpg", ".jpeg", ".png"}, f"{url} {src}")
                anchor = full_anchor(ancestors)
                if anchor and (match := FULL_SIZE.search(anchor.get("aria-label", ""))):
                    source_width = int(match.group(1))
                else:
                    source_width = int(img["width"])
                original = self.originals[anchor["href"]] if anchor else self.originals[src]
                widths = expected_widths(source_width)
                webps = [source for source in sources if source.get("type") == "image/webp"]
                if original.suffix.lower() in {".jpg", ".jpeg"}:
                    self.assertEqual(len(webps), 1, f"{url} {src}")
                    self.assertEqual(srcset_widths(webps[0]["srcset"]), widths, f"{url} {src}")
                else:
                    self.assertLessEqual(len(webps), 1, f"{url} {src}")
                    if webps:
                        self.assertEqual(srcset_widths(webps[0]["srcset"]), widths, f"{url} {src}")
                        for part in webps[0]["srcset"].split(","):
                            url_part = part.strip().split()[0]
                            webp = ROOT / "public" / url_part.lstrip("/")
                            width = int(SRCSET_WIDTH.search(part).group(1))
                            fb = next(
                                piece.strip().split()[0]
                                for piece in img.get("srcset", f"{src} {width}w").split(",")
                                if SRCSET_WIDTH.search(piece) and int(SRCSET_WIDTH.search(piece).group(1)) == width
                            )
                            fb_path = ROOT / "public" / fb.lstrip("/")
                            self.assertLess(webp.stat().st_size, fb_path.stat().st_size, url_part)
                checked += 1
        self.assertGreater(checked, 100)

    def test_click_through_href_is_the_committed_original(self):
        for url, images in articles():
            for img, ancestors, _ in images:
                src = img.get("src", "")
                if src.startswith(("http://", "https://", "//")):
                    continue
                anchor = full_anchor(ancestors)
                if anchor:
                    href = anchor["href"]
                    self.assertNotIn("_hu_", href, f"{url} {src}")
                    self.assertIn(href, self.originals, f"{url} {src}")
                    label = FULL_SIZE.search(anchor.get("aria-label", ""))
                    self.assertIsNotNone(label, f"{url} {src}")
                    original_width = int(label.group(1))
                    if original_width <= COLUMN:
                        # Same-width heavy re-encode: the page shows a
                        # smaller file than the master it links to.
                        shown = ROOT / "public" / src.lstrip("/")
                        master = self.originals[href]
                        self.assertGreater(master.stat().st_size, shown.stat().st_size, f"{url} {src}")
                else:
                    self.assertNotIn("_hu_", src, f"{url} {src}")
                    self.assertEqual(mat_kind(ancestors), "mat", f"{url} {src}")

    def test_legacy_500px_master_is_a_mat_not_a_link(self):
        images = images_in(read("/2013/5-am/index.html"))
        sketch = next(item for item in images if item[0]["src"].endswith("/luffy-sketch.jpg"))
        img, ancestors, sources = sketch
        self.assertNotIn("_hu_", img["src"])
        self.assertIsNone(full_anchor(ancestors))
        self.assertEqual(mat_kind(ancestors), "mat")
        self.assertNotIn("srcset", img)
        self.assertEqual(img["width"], "500")
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["type"], "image/webp")
        self.assertEqual(srcset_widths(sources[0]["srcset"]), [500])
        webp = sources[0]["srcset"].split()[0]
        self.assertTrue(webp.startswith("/img/"), webp)
        self.assertTrue(webp.endswith(".webp"), webp)

    def test_gif_is_unlinked_and_unprocessed(self):
        images = images_in(read("/2020/dont-waste-time-getting-feedback/index.html"))
        img, ancestors, sources = images[0]
        self.assertTrue(img["src"].endswith("/hourglass.gif"), img["src"])
        self.assertNotIn("_hu_", img["src"])
        self.assertEqual(sources, [])
        self.assertNotIn("srcset", img)
        self.assertEqual(mat_kind(ancestors), "mat")
        self.assertIsNone(full_anchor(ancestors))
        self.assertEqual(img["loading"], "eager")
        self.assertTrue(img.get("width") and img.get("height"))

    def test_heavy_native_photo_links_to_the_original(self):
        images = images_in(read("/2022/journaling-the-best-habit-i-picked-up-in-2021/index.html"))
        sketch = next(item for item in images if "writing-sketch" in item[0]["src"])
        self.assertIsNone(full_anchor(sketch[1]))
        self.assertEqual(mat_kind(sketch[1]), "mat")
        self.assertEqual(sketch[0]["loading"], "eager")

        photo = next(item for item in images if "my-journal" in item[0]["src"])
        img, ancestors, sources = photo
        anchor = full_anchor(ancestors)
        self.assertTrue(anchor["href"].endswith("/my-journal.jpg"), anchor["href"])
        self.assertNotIn("_hu_", anchor["href"])
        self.assertIn("_hu_", img["src"])
        self.assertTrue(img["src"].startswith("/img/"), img["src"])
        self.assertEqual(img["width"], "1486")
        self.assertEqual(img["height"], "1982")
        original = self.originals[anchor["href"]]
        shown = ROOT / "public" / img["src"].lstrip("/")
        self.assertGreater(original.stat().st_size, HEAVY_BYTES)
        self.assertLess(shown.stat().st_size, original.stat().st_size)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["type"], "image/webp")

        app = next(item for item in images if "day-one-app" in item[0]["src"])
        self.assertIsNotNone(full_anchor(app[1]))
        self.assertNotIn("_hu_", full_anchor(app[1])["href"])
        self.assertEqual(app[0]["width"], "1500")
        self.assertTrue(app[0]["src"].endswith(".png"), app[0]["src"])

    def test_wide_photo_displays_a_downscale_and_links_the_original(self):
        images = images_in(read("/2012/saying-goodbye-to-the-bay-area/index.html"))
        linked = [item for item in images if full_anchor(item[1])]
        self.assertGreaterEqual(len(linked), 4)
        for img, ancestors, _ in linked:
            anchor = full_anchor(ancestors)
            label = FULL_SIZE.search(anchor["aria-label"])
            self.assertGreater(int(label.group(1)), MAX_WIDTH)
            self.assertEqual(img["width"], str(MAX_WIDTH))
            self.assertIn("_hu_", img["src"])
            self.assertNotIn("_hu_", anchor["href"])
            shown = ROOT / "public" / img["src"].lstrip("/")
            self.assertLess(shown.stat().st_size, self.originals[anchor["href"]].stat().st_size)

    def test_hashed_derivatives_are_immutable_and_originals_are_not(self):
        rules = raw_rules(ROOT / "static" / "_headers")
        headers = matcher(rules)
        originals = set(self.originals)
        hashed = []
        for dirpath, _, filenames in os.walk(ROOT / "public" / "img"):
            for name in filenames:
                path = Path(dirpath) / name
                url = "/" + path.relative_to(ROOT / "public").as_posix()
                self.assertIn("_hu_", name, url)
                self.assertEqual(headers(url).get("cache-control"), IMMUTABLE, url)
                hashed.append(url)
        self.assertGreater(len(hashed), 100)

        published = []
        for url, path in self.originals.items():
            built = ROOT / "public" / url.lstrip("/")
            if not built.is_file():
                continue
            published.append(url)
            self.assertNotIn("_hu_", url)
            self.assertEqual(headers(url).get("cache-control"), [], url)
            self.assertEqual(built.stat().st_size, path.stat().st_size, url)
        self.assertGreater(len(published), 100)
        self.assertTrue(originals)

        static_hashed = []
        for dirpath, _, filenames in os.walk(ROOT / "public" / "static"):
            for name in filenames:
                if "_hu_" not in name:
                    continue
                url = "/" + (Path(dirpath) / name).relative_to(ROOT / "public").as_posix()
                static_hashed.append(url)
                self.assertEqual(len(headers(url).get("cache-control", [])), 1, url)
        self.assertTrue(static_hashed)
