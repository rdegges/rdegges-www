"""The About page is a standalone page, not a post."""

import html
import os
import unittest
from html.parser import HTMLParser

from helpers import PUBLIC, SiteTestCase, articles, pages, public_file


def jpeg_size(path):
    """Pixel size of a baseline or progressive JPEG, read from the SOF marker."""
    data = open(path, "rb").read()
    if not data.startswith(b"\xff\xd8"):
        raise AssertionError(f"not a jpeg: {path}")
    i = 2
    while i < len(data) - 8:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        if marker == 0xDA:
            break
        seglen = int.from_bytes(data[i + 2 : i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2):
            height = int.from_bytes(data[i + 5 : i + 7], "big")
            width = int.from_bytes(data[i + 7 : i + 9], "big")
            return width, height
        i += 2 + seglen
    raise AssertionError(f"no jpeg frame size in {path}")


class Text(HTMLParser):
    """Element text, which helpers.Page does not keep."""

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self._capture = None
        self.parts = []  # (tag, attrs, text)
        with open(path, encoding="utf-8") as f:
            self.feed(f.read())

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "figcaption", "a"):
            self._capture = [tag, dict(attrs), ""]
            self.parts.append(self._capture)

    def handle_endtag(self, tag):
        if self._capture and tag == self._capture[0]:
            self._capture[2] = " ".join(self._capture[2].split())
            self._capture = None

    def handle_data(self, data):
        if self._capture:
            self._capture[2] += data


class TestAbout(SiteTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page = next(p for p in pages() if p.url == "/about/")
        with open(cls.page.path, encoding="utf-8") as f:
            cls.html = f.read()

    def test_is_its_own_page(self):
        self.assertTrue(os.path.isfile(self.page.path))
        self.assertEqual(self.page.title, "About - Randall Degges")
        self.assertEqual(
            self.page.meta("description"),
            "Randall Degges is VP of AI Engineering at Snyk and a self-taught programmer."
            " Previously Okta and Stormpath; creator of ipify.",
        )
        h1 = [text for tag, _, text in Text(self.page.path).parts if tag == "h1"]
        self.assertEqual(h1, ["About"])
        # No dateline, and it is not offered as a Markdown post.
        self.assertEqual(self.page.find("time"), [])
        self.assertEqual(self.page.find("p", **{"class": "post-date"}), [])
        self.assertNotIn("If you read this far", self.html)
        self.assertEqual(self.page.find("link", type="text/markdown"), [])
        self.assertFalse(os.path.exists(os.path.join(PUBLIC, "about", "index.md")))

    def test_posts_still_show_a_date_and_the_subscribe_note(self):
        # showDate / showSubscribe default to on. Hiding them for About must
        # not hide them for every post.
        post = next(p for p in articles())
        with open(post.path, encoding="utf-8") as f:
            post_html = f.read()
        self.assertTrue(post.find("p", **{"class": "post-date"}))
        self.assertIn("If you read this far", post_html)

    def test_not_listed_with_the_posts_or_the_feed(self):
        home = next(p for p in pages() if p.url == "/")
        with open(home.path, encoding="utf-8") as f:
            main = f.read().split("<main", 1)[1].split("</main>", 1)[0]
        self.assertNotIn("/about/", main)
        with open(os.path.join(PUBLIC, "feed.xml"), encoding="utf-8") as f:
            feed = f.read()
        self.assertNotIn("/about/", feed)
        with open(os.path.join(PUBLIC, "llms.txt"), encoding="utf-8") as f:
            posts = f.read().split("\n## Posts\n", 1)[1]
        self.assertNotIn("/about/", posts)

    def test_nav_links_to_about(self):
        links = [a for a in self.page.find("a") if a.get("href") == "/about/"]
        self.assertTrue(links, "no nav link to /about/")
        # The nav partial uppercases the label. Confirm it on the raw text.
        labels = [text for tag, attrs, text in Text(self.page.path).parts if tag == "a" and attrs.get("href") == "/about/"]
        self.assertIn("ABOUT", labels)

    def test_copy_matches_the_approved_bio(self):
        # Goldmark's typographer turns apostrophes and -- into entities.
        # Compare the text a reader sees, not the encoded source.
        text = html.unescape(self.html).replace("\u2019", "'").replace("\u2013", "--")
        for phrase in (
            "today I'm VP of AI Engineering",
            "https://snyk.io",
            "https://workos.com",
            "https://www.arcade.dev",
            "https://www.onehouse.ai",
            "https://www.builder.io",
            "https://www.ragie.ai",
            "https://ipify.org",
            "https://haveibeenpwned.com/",
            "https://hardlyfunny.com",
            "The Heroku Hacker's Guide",
            "I live in Bend, Oregon",
            "super cute dog named Dandelion",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        # The current role is VP of AI Engineering, not Developer Relations.
        self.assertNotIn("Developer Relations", text)
        mailtos = {a.get("href") for a in self.page.find("a") if (a.get("href") or "").startswith("mailto:")}
        self.assertEqual(mailtos, {"mailto:r@rdegges.com"})
        # The Bend sentence is a paragraph beside the patio photo, same as the others.
        self.assertRegex(self.html, r"<p>[^<]*I live in Bend, Oregon")

    def test_photos_link_to_the_full_originals(self):
        text = Text(self.page.path)
        captions = [t for tag, _, t in text.parts if tag == "figcaption"]
        self.assertEqual(
            captions,
            [
                "On stage at AI Engineer World's Fair, San Francisco, 2026",
                "Dandelion and Samantha",
            ],
        )
        figures = self.page.find("figure")
        self.assertEqual(
            [f.get("class") for f in figures],
            ["about-photo float-right", "about-photo float-left"],
        )
        self.assertEqual(len(self.page.find("div", id="personal-block")), 1)
        self.assertTrue(self.page.find("div", **{"class": "clear"}))

        # Both squares are print-mat links, including the 600px stage frame,
        # which is narrower than the column and would otherwise be span.img-mat.
        hrefs = [a.get("href") for a in self.page.find("a", **{"class": "img-full"})]
        self.assertEqual(len(hrefs), 2)
        self.assertEqual(self.page.find("span", **{"class": "img-mat"}), [])
        expected = {
            "/about/ai-engineer-worlds-fair-2026.jpg": (600, 400),
            "/about/samantha-and-dandelion-patio.jpg": (2048, 1536),
        }
        self.assertEqual(hrefs, list(expected))
        content_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "content", "about"))
        for href, size in expected.items():
            with self.subTest(href=href):
                path = public_file(href)
                self.assertTrue(os.path.isfile(path), href)
                self.assertEqual(jpeg_size(path), size)
                # The click target is the committed original, byte for byte, not a resized crop.
                self.assertNotIn("_hu_", os.path.basename(path))
                with open(os.path.join(content_dir, os.path.basename(href)), "rb") as f:
                    original = f.read()
                with open(path, "rb") as f:
                    published = f.read()
                self.assertEqual(published, original)

        alts = [img.get("alt") for img in self.page.find("img")]
        # The render hook's typographer curls the apostrophe in alt text.
        self.assertEqual(
            alts,
            [
                "Me speaking on stage at AI Engineer World\u2019s Fair 2026",
                "My wife Samantha holding our dog Dandelion on a patio",
            ],
        )
        # The stage photo is the one above the fold.
        imgs = self.page.find("img")
        self.assertEqual(imgs[0].get("loading"), "eager")
        self.assertEqual(imgs[0].get("fetchpriority"), "high")
        self.assertEqual(imgs[1].get("loading"), "lazy")

    def test_is_in_the_sitemap(self):
        # build.list "never" keeps About out of the post list, the feed and
        # llms.txt's Posts -- and out of Hugo's sitemap too, so search engines
        # only found it by following the nav link.
        import xml.etree.ElementTree as ET

        root = ET.parse(public_file("/sitemap.xml")).getroot()
        locs = [loc.text for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(locs.count("https://rdegges.com/about/"), 1)

    def test_is_linked_from_llms_txt(self):
        with open(public_file("/llms.txt"), encoding="utf-8") as f:
            text = f.read()
        pages = text.split("\n## Pages\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("- [About](https://rdegges.com/about/): ", pages)

    def test_is_not_listed_as_a_post(self):
        # About is in Hugo's page collections now, so the post list, the feed
        # and llms.txt's Posts each have to leave it out themselves.
        with open(public_file("/index.html"), encoding="utf-8") as f:
            # The nav links /about/; the post list uses absolute permalinks.
            # (The Person schema's photo lives under /about/, so match the page URL only.)
            self.assertNotRegex(f.read(), r"https://rdegges\.com/about/(?![\w.-])")
        with open(public_file("/feed.xml"), encoding="utf-8") as f:
            self.assertNotIn("https://rdegges.com/about/", f.read())
        with open(public_file("/llms.txt"), encoding="utf-8") as f:
            self.assertNotIn("/about/", f.read().split("\n## Posts\n", 1)[1])

    def test_share_title_names_the_person(self):
        # An unfurl that just says "About" does not say about whom.
        self.assertEqual(self.page.meta("og:title"), "About - Randall Degges")

    def test_stylesheet_crops_the_photos_square(self):
        href = self.page.find("link", rel="stylesheet")[0]["href"]
        css = open(public_file(href), encoding="utf-8").read()
        self.assertIn("aspect-ratio:1/1", css.replace(" ", ""))
        self.assertIn("object-fit:cover", css.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
