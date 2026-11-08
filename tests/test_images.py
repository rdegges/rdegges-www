"""Images reserve their space, wear a print mat, and offer a safe fallback.

The render hook builds the markup these tests read. Every article image is
matted. The wrapper is a link when the original is wider than the content
column, the page sets linkOriginals, or the file on the page is a lighter
re-encode of a heavy master. The href is the committed original. Photos add
a WebP <picture> inside that wrapper; the <img> stays a JPEG or PNG.
"""

import glob
import os
import re
import unittest
from html.parser import HTMLParser

from helpers import PUBLIC, SiteTestCase, articles, pages, public_file
from test_headers import matcher, raw_rules

CONTENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "content"))

# The hook's ladder, copied here so a silent edit to either side fails.
COLUMN = 750
LADDER = (480, 750, 1125)
CAP = 1500

FULL_SIZE = re.compile(r"view full size \((\d+)×(\d+)\)")
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}


def expected_widths(source_width):
    """Candidate widths the hook emits for a master of this width."""
    cap = min(source_width, CAP)
    widths = [w for w in LADDER if w * 100 < cap * 85]
    widths.append(cap)
    return widths


def srcset(value):
    """[(url, width or None)] from a srcset attribute."""
    found = []
    for part in (value or "").split(","):
        part = part.strip()
        if not part:
            continue
        bits = part.split()
        width = int(bits[1][:-1]) if len(bits) > 1 and bits[1].endswith("w") else None
        found.append((bits[0], width))
    return found


def classes(attrs):
    return set((attrs.get("class") or "").split())


def cache_control(url):
    """Cache-Control values Cloudflare would send for url, in file order."""
    values = []
    for pattern, headers in raw_rules():
        if matcher(pattern).match(url):
            values += [value for _, name, value in headers if name == "cache-control"]
    return values


class ImageParents(HTMLParser):
    """Each img, its ancestors, and the <source> elements in its <picture>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "source":
            for frame in reversed(self.stack):
                if frame[0] == "picture":
                    frame[2].append(attrs)
                    break
            return
        if tag == "img":
            sources = []
            picture_depth = None
            anchor = None
            anchor_depth = None
            for depth, (parent, parent_attrs, parent_sources) in enumerate(reversed(self.stack)):
                if picture_depth is None and parent == "picture":
                    picture_depth = depth
                    sources = list(parent_sources)
                if anchor is None and parent == "a" and "img-full" in classes(parent_attrs):
                    anchor = parent_attrs
                    anchor_depth = depth
            self.images.append(
                {
                    "attrs": attrs,
                    "ancestors": [(parent, parent_attrs) for parent, parent_attrs, _ in self.stack],
                    "sources": sources,
                    "picture_depth": picture_depth,
                    "anchor": anchor,
                    "anchor_depth": anchor_depth,
                }
            )
            return
        if tag not in VOID:
            self.stack.append((tag, attrs, []))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


def images_in(page):
    parser = ImageParents()
    with open(page.path, encoding="utf-8") as f:
        parser.feed(f.read())
    return parser.images


def mat_kind(ancestors):
    """'full' or 'mat' for the print-mat wrapper, looking through <picture>."""
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


def article_images():
    for page in articles():
        for image in images_in(page):
            yield page, image


def original_urls():
    """URL paths of the JPEG/PNG/GIF masters, at the URL Hugo publishes.

    The directory under content/ is not always the public slug: a post can
    set `slug` in front matter and the files move with it.
    """
    urls = []
    indexes = glob.glob(os.path.join(CONTENT, "*", "*", "index.md"))
    indexes += glob.glob(os.path.join(CONTENT, "*", "index.md"))
    for index in indexes:
        with open(index, encoding="utf-8") as f:
            front = f.read().split("---\n", 2)[1]
        slug = re.search(r'^slug:\s*"?([^"\n]+)"?\s*$', front, re.M)
        bundle = os.path.dirname(index)
        parent = os.path.dirname(bundle)
        slug = slug.group(1) if slug else os.path.basename(bundle)
        if os.path.abspath(parent) == CONTENT:
            prefix = f"/{slug}"
        else:
            prefix = f"/{os.path.basename(parent)}/{slug}"
        for root, _, files in os.walk(bundle):
            for name in files:
                if os.path.splitext(name)[1].lower() not in {".jpg", ".jpeg", ".png", ".gif"}:
                    continue
                rel = os.path.relpath(os.path.join(root, name), bundle).replace(os.sep, "/")
                urls.append(f"{prefix}/{rel}")
    return urls


class TestImages(SiteTestCase):
    def test_every_image_declares_its_size(self):
        # width/height let the browser reserve the box before the file
        # arrives, which is what keeps layout shift at zero.
        for page in pages():
            for img in page.find("img"):
                with self.subTest(page=page.url, img=img.get("src")):
                    self.assertTrue(img.get("width") and img.get("height"))

    def test_home_avatar_is_small_and_high_priority(self):
        home = next(p for p in pages() if p.url == "/")
        avatar = home.find("img")[0]
        self.assertEqual(avatar.get("fetchpriority"), "high")
        self.assertNotEqual(avatar.get("loading"), "lazy")
        candidates = [c.split()[0] for c in avatar["srcset"].split(",")] + [avatar["src"]]
        for src in candidates:
            with self.subTest(src=src):
                self.assertLess(os.path.getsize(public_file(src)), 40_000)

    def test_article_images_are_matted_and_only_some_are_links(self):
        # The mat wraps the picture, or the img when there is no picture.
        # A link carries an accessible name. A plain mat is not a link.
        seen = 0
        for page in articles():
            for image in images_in(page):
                seen += 1
                attrs = image["attrs"]
                kind = mat_kind(image["ancestors"])
                with self.subTest(page=page.url, img=attrs.get("src")):
                    self.assertIn(kind, ("full", "mat"))
                    if image["sources"]:
                        self.assertEqual(image["ancestors"][-1][0], "picture")
                        if image["anchor"]:
                            self.assertLess(image["picture_depth"], image["anchor_depth"])
                    if kind == "full":
                        self.assertIsNotNone(image["anchor"])
                        self.assertTrue(image["anchor"].get("href"))
                        self.assertNotIn("_hu_", image["anchor"]["href"])
                        self.assertIn("view full size", image["anchor"].get("aria-label", ""))
                    else:
                        self.assertIsNone(image["anchor"])
        self.assertGreater(seen, 100)

    def test_originals_wider_than_the_column_link(self):
        # The page shows an image at the content column, about 750 CSS px.
        # Wider originals link; a file the column already shows at full
        # size does not. The 1500px figure is only the inline srcset cap.
        # The href is the committed original, never a hashed derivative.
        by_url = {p.url: p for p in articles()}

        goodbye = images_in(by_url["/2015/saying-goodbye/"])
        resized = [
            image for image in goodbye
            if image["anchor"] and image["anchor"].get("href") != image["attrs"].get("src")
        ]
        self.assertTrue(resized, "a photo wider than the srcset cap still links to a different file")
        for image in resized:
            label = image["anchor"]["aria-label"]
            self.assertGreater(int(FULL_SIZE.search(label).group(1)), CAP)
            self.assertNotIn("_hu_", image["anchor"]["href"])

        grim = images_in(by_url["/2024/im-writing-again/"])
        self.assertEqual(len(grim), 1)
        self.assertIn("grim-reaper-writing-sketch", grim[0]["attrs"]["src"])
        self.assertEqual(mat_kind(grim[0]["ancestors"]), "full")
        self.assertNotIn("_hu_", grim[0]["anchor"]["href"])
        self.assertIn("grim-reaper-writing-sketch", grim[0]["anchor"]["href"])

        journal = images_in(by_url["/2022/journaling-the-best-habit-i-picked-up-in-2021/"])
        photo = next(image for image in journal if "my-journal" in image["attrs"]["src"])
        self.assertEqual(mat_kind(photo["ancestors"]), "full")
        self.assertTrue(photo["anchor"]["href"].endswith("/my-journal.jpg"), photo["anchor"]["href"])
        self.assertNotIn("_hu_", photo["anchor"]["href"])

        luffy = images_in(by_url["/2013/5-am/"])
        self.assertEqual(len(luffy), 1)
        self.assertIn("luffy-sketch", luffy[0]["attrs"]["src"])
        self.assertEqual(mat_kind(luffy[0]["ancestors"]), "mat")

        graphql = images_in(by_url["/2021/how-i-converted-a-rest-api-to-graphql/"])
        gif = next(image for image in graphql if "rest-to-graphql" in image["attrs"]["src"])
        self.assertEqual(mat_kind(gif["ancestors"]), "mat")
        self.assertTrue(any(mat_kind(image["ancestors"]) == "full" for image in graphql))

    def test_the_mat_does_not_wrap_the_avatar(self):
        # The avatar, favicons, and other chrome are not article images.
        # /about/ is a page, not a post, but its photos use the same mat.
        for page in pages():
            if page in articles() or page.url == "/about/":
                continue
            for image in images_in(page):
                with self.subTest(page=page.url, img=image["attrs"].get("src")):
                    self.assertIsNone(mat_kind(image["ancestors"]))

    def test_stylesheet_carries_the_mat_and_expand_mark(self):
        # The mark is a CSS pseudo-element. Minify may rewrite numbers, but
        # the mat, the zoom cursor, and the two arrow strokes have to survive.
        hrefs = {a["href"] for p in pages() for a in p.find("link", rel="stylesheet")}
        css = ""
        for href in hrefs:
            with open(public_file(href), encoding="utf-8") as f:
                css += f.read()
        self.assertIn("img-mat", css)
        self.assertIn("zoom-in", css)
        self.assertIn("fit-content", css)
        self.assertIn("#d0d0d0", css)
        self.assertIn("focus-visible", css)
        self.assertIn("img-mat picture", css)
        self.assertTrue(
            "M9.5 2.5" in css or "M9.5%202.5" in css,
            "expand-mark svg missing from the stylesheet",
        )
        self.assertNotIn("img-full:focus-visible{outline:none", css.replace(" ", ""))
        self.assertNotIn("img-full:focus-visible{outline:0", css.replace(" ", ""))

    def test_article_images_keep_loading_and_dimensions(self):
        seen = 0
        for page in articles():
            images = images_in(page)
            if not images:
                continue
            seen += 1
            for i, image in enumerate(images):
                attrs = image["attrs"]
                with self.subTest(page=page.url, src=attrs.get("src")):
                    self.assertEqual(attrs.get("decoding"), "async")
                    width, height = int(attrs["width"]), int(attrs["height"])
                    self.assertGreater(width, 0)
                    self.assertGreater(height, 0)
                    ext = os.path.splitext(attrs["src"])[1].lower()
                    if ext != ".gif":
                        self.assertLessEqual(width, CAP)
                    if i == 0:
                        self.assertEqual(attrs.get("loading"), "eager")
                        self.assertEqual(attrs.get("fetchpriority"), "high")
                    else:
                        self.assertEqual(attrs.get("loading"), "lazy")
                        self.assertNotEqual(attrs.get("fetchpriority"), "high")
        self.assertGreater(seen, 100)

    def test_candidates_follow_the_ladder_and_never_upscale(self):
        checked = 0
        for page, image in article_images():
            attrs = image["attrs"]
            ext = os.path.splitext(attrs["src"])[1].lower()
            if ext == ".gif":
                self.assertEqual(image["sources"], [], attrs["src"])
                self.assertNotIn("srcset", attrs)
                continue
            anchor = image["anchor"]
            if anchor:
                match = FULL_SIZE.search(anchor.get("aria-label") or "")
                self.assertIsNotNone(match, anchor.get("aria-label"))
                source_width = int(match.group(1))
                source_height = int(match.group(2))
            else:
                source_width = int(attrs["width"])
                source_height = int(attrs["height"])
            want = expected_widths(source_width)
            got = [w for _, w in srcset(attrs.get("srcset"))]
            with self.subTest(page=page.url, src=attrs["src"]):
                self.assertEqual(int(attrs["width"]), min(source_width, CAP))
                self.assertEqual(int(attrs["width"]), want[-1])
                if len(want) == 1:
                    self.assertNotIn("srcset", attrs)
                    self.assertNotIn("sizes", attrs)
                else:
                    self.assertEqual(got, want)
                    self.assertIn("sizes", attrs)
                self.assertGreaterEqual(source_width, int(attrs["width"]))
                expect_h = round(source_height * int(attrs["width"]) / source_width)
                self.assertLessEqual(abs(int(attrs["height"]) - expect_h), 1)
                for candidate in got:
                    self.assertLessEqual(candidate, source_width)
                    self.assertLessEqual(candidate, CAP)
            checked += 1
        self.assertGreater(checked, 100)

    def test_picture_has_a_webp_source_and_a_raster_fallback(self):
        # The img is what a client that ignores <picture> and srcset fetches.
        # It stays a JPEG or PNG, and it is never the only thing a supporting
        # browser is offered for a photo.
        photos = pngs = 0
        for page, image in article_images():
            attrs = image["attrs"]
            src = attrs["src"]
            ext = os.path.splitext(src)[1].lower()
            if ext == ".gif":
                self.assertFalse(image["sources"])
                continue
            self.assertIn(ext, {".jpg", ".jpeg", ".png"}, src)
            self.assertNotIn(".avif", src)
            href = (image["anchor"] or {}).get("href") or src
            original_ext = os.path.splitext(href)[1].lower()
            with self.subTest(page=page.url, src=src):
                if original_ext in {".jpg", ".jpeg"}:
                    photos += 1
                    self.assertEqual(len(image["sources"]), 1)
                if image["sources"]:
                    self.assertEqual(len(image["sources"]), 1, "AVIF is out of scope")
                    source = image["sources"][0]
                    self.assertEqual(source.get("type"), "image/webp")
                    webp = srcset(source.get("srcset"))
                    fallback = srcset(attrs.get("srcset"))
                    if fallback:
                        self.assertEqual([w for _, w in webp], [w for _, w in fallback])
                        self.assertEqual(source.get("sizes"), attrs.get("sizes"))
                    else:
                        self.assertEqual(len(webp), 1)
                        self.assertEqual(webp[0][1], int(attrs["width"]))
                    for url, _ in webp:
                        self.assertTrue(url.endswith(".webp"), url)
                        self.assertTrue(url.startswith("/img/"), url)
                    if ext == ".png":
                        pngs += 1
                        by_width = {w: url for url, w in fallback} if fallback else {int(attrs["width"]): src}
                        for url, width in webp:
                            png_url = by_width[width]
                            self.assertLess(
                                os.path.getsize(public_file(url)),
                                os.path.getsize(public_file(png_url)),
                                f"{url} is not smaller than {png_url}",
                            )
        self.assertGreater(photos, 50)
        self.assertGreater(pngs, 10)

    def test_click_through_href_is_the_committed_original(self):
        # Wider than the column, or a same-width file that is not the master
        # because a heavy original was re-encoded. GIFs never link. A file
        # the column already shows at full size does not either.
        linked = unlinked = 0
        for page, image in article_images():
            attrs = image["attrs"]
            src = attrs["src"]
            anchor = image["anchor"]
            ext = os.path.splitext(src)[1].lower()
            with self.subTest(page=page.url, src=src):
                if ext == ".gif":
                    self.assertIsNone(anchor)
                    self.assertNotIn("_hu_", src)
                    self.assertEqual(mat_kind(image["ancestors"]), "mat")
                    unlinked += 1
                    continue
                if anchor:
                    linked += 1
                    self.assertEqual(anchor.get("class"), "img-full")
                    href = anchor["href"]
                    self.assertNotEqual(href, "")
                    self.assertNotIn("_hu_", href)
                    self.assertTrue(os.path.isfile(public_file(href)), href)
                    match = FULL_SIZE.search(anchor.get("aria-label") or "")
                    self.assertIsNotNone(match, anchor.get("aria-label"))
                    original_w = int(match.group(1))
                    displayed_w = int(attrs["width"])
                    self.assertGreaterEqual(original_w, displayed_w)
                    if original_w <= COLUMN:
                        self.assertEqual(original_w, displayed_w)
                        self.assertGreater(
                            os.path.getsize(public_file(href)),
                            os.path.getsize(public_file(src)),
                        )
                else:
                    unlinked += 1
                    self.assertNotIn("_hu_", src)
                    self.assertEqual(mat_kind(image["ancestors"]), "mat")
                    self.assertLessEqual(int(attrs["width"]), COLUMN)
        self.assertGreater(linked, 10)
        self.assertGreater(unlinked, 50)

    def test_legacy_500px_master_is_a_mat_not_a_link(self):
        page = next(p for p in articles() if p.url == "/2013/5-am/")
        images = images_in(page)
        sketch = next(i for i in images if "luffy-sketch" in i["attrs"]["src"])
        attrs = sketch["attrs"]
        self.assertTrue(attrs["src"].endswith("/luffy-sketch.jpg"), attrs["src"])
        self.assertNotIn("_hu_", attrs["src"])
        self.assertIsNone(sketch["anchor"])
        self.assertEqual(mat_kind(sketch["ancestors"]), "mat")
        # One width, so the img has no srcset. It is still a photo, so a
        # same-width WebP is offered beside the original JPEG.
        self.assertNotIn("srcset", attrs)
        self.assertEqual(attrs["width"], "500")
        self.assertEqual(len(sketch["sources"]), 1)
        webp = srcset(sketch["sources"][0].get("srcset"))
        self.assertEqual([w for _, w in webp], [500])
        self.assertTrue(webp[0][0].startswith("/img/") and webp[0][0].endswith(".webp"))

    def test_gif_bypasses_processing(self):
        page = next(p for p in articles() if p.url == "/2020/dont-waste-time-getting-feedback/")
        image = images_in(page)[0]
        attrs = image["attrs"]
        self.assertTrue(attrs["src"].endswith("/hourglass.gif"), attrs["src"])
        self.assertNotIn("_hu_", attrs["src"])
        self.assertIsNone(image["anchor"])
        self.assertEqual(mat_kind(image["ancestors"]), "mat")
        self.assertFalse(image["sources"])
        self.assertNotIn("srcset", attrs)
        self.assertEqual(attrs.get("loading"), "eager")
        self.assertTrue(attrs.get("width") and attrs.get("height"))

    def test_heavy_journal_photo_is_a_same_width_derivative(self):
        # 1486px is under the 1500 cap, but the master is ~980 KB. Display
        # uses a lighter encode; the click still reaches the master.
        page = next(p for p in articles() if p.url == "/2022/journaling-the-best-habit-i-picked-up-in-2021/")
        images = images_in(page)
        journal = next(i for i in images if "my-journal" in (i["anchor"] or {}).get("href", ""))
        attrs = journal["attrs"]
        href = journal["anchor"]["href"]
        self.assertTrue(href.endswith("/my-journal.jpg"), href)
        self.assertNotIn("_hu_", href)
        self.assertIn("_hu_", attrs["src"])
        self.assertTrue(attrs["src"].startswith("/img/"))
        self.assertEqual(attrs["width"], "1486")
        self.assertEqual(attrs["height"], "1982")
        self.assertGreater(os.path.getsize(public_file(href)), 500_000)
        self.assertLess(os.path.getsize(public_file(attrs["src"])), os.path.getsize(public_file(href)))
        self.assertEqual(journal["sources"][0].get("type"), "image/webp")
        # The sketch is narrower than the column, so it keeps the mat only.
        sketch = images[0]
        self.assertIn("writing-sketch.png", sketch["attrs"]["src"])
        self.assertIsNone(sketch["anchor"])
        self.assertEqual(mat_kind(sketch["ancestors"]), "mat")
        self.assertEqual(sketch["attrs"].get("loading"), "eager")
        screenshot = next(i for i in images if "day-one-app" in (i["anchor"] or {}).get("href", ""))
        self.assertEqual(screenshot["attrs"]["width"], "1500")
        self.assertTrue(screenshot["attrs"]["src"].endswith(".png"))
        self.assertNotIn("_hu_", screenshot["anchor"]["href"])

    def test_wide_photo_links_to_the_original_and_displays_the_cap(self):
        page = next(p for p in articles() if p.url == "/2015/saying-goodbye/")
        linked = [i for i in images_in(page) if i["anchor"]]
        wide = []
        for image in linked:
            match = FULL_SIZE.search(image["anchor"]["aria-label"])
            if int(match.group(1)) > CAP:
                wide.append(image)
        self.assertGreater(len(wide), 5)
        for image in wide:
            attrs = image["attrs"]
            with self.subTest(src=attrs["src"]):
                self.assertEqual(attrs["width"], str(CAP))
                self.assertIn("_hu_", attrs["src"])
                self.assertNotIn("_hu_", image["anchor"]["href"])
                self.assertLess(
                    os.path.getsize(public_file(attrs["src"])),
                    os.path.getsize(public_file(image["anchor"]["href"])),
                )
        # A file between the column and the cap still links, and it is shown
        # at its own width. 1500 is not the link threshold.
        mid = [i for i in linked if i not in wide]
        self.assertTrue(mid)
        for image in mid:
            attrs = image["attrs"]
            original_w = int(FULL_SIZE.search(image["anchor"]["aria-label"]).group(1))
            with self.subTest(src=attrs["src"]):
                self.assertGreater(original_w, COLUMN)
                self.assertEqual(attrs["width"], str(original_w))
                self.assertNotIn("_hu_", image["anchor"]["href"])

    def test_hashed_derivatives_are_immutable_and_originals_are_not(self):
        derivatives = []
        img_root = os.path.join(PUBLIC, "img")
        for root, _, files in os.walk(img_root):
            for name in files:
                url = "/" + os.path.relpath(os.path.join(root, name), PUBLIC).replace(os.sep, "/")
                derivatives.append(url)
        self.assertGreater(len(derivatives), 50)
        for url in derivatives:
            with self.subTest(url=url):
                self.assertIn("_hu_", os.path.basename(url))
                self.assertEqual(cache_control(url), ["public, max-age=31536000, immutable"])

        originals = original_urls()
        self.assertGreater(len(originals), 100)
        for url in originals:
            with self.subTest(url=url):
                self.assertNotIn("_hu_", url)
                self.assertTrue(os.path.isfile(public_file(url)), url)
                self.assertEqual(cache_control(url), [])

        # The two rules do not stack: /static/* already caches the avatar.
        static_derivative = None
        for root, _, files in os.walk(os.path.join(PUBLIC, "static")):
            for name in files:
                if "_hu_" in name:
                    static_derivative = "/" + os.path.relpath(
                        os.path.join(root, name), PUBLIC
                    ).replace(os.sep, "/")
                    break
        self.assertIsNotNone(static_derivative)
        self.assertEqual(len(cache_control(static_derivative)), 1)


if __name__ == "__main__":
    unittest.main()
