"""One <h1> per page, and it's the page's own subject."""

import unittest
from html.parser import HTMLParser

from helpers import SiteTestCase, articles, pages

HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")
SITE_NAME = "RANDALL DEGGES"  # {{ upper .Site.Title }}
TAGLINE = "Random Thoughts of a Happy Programmer"


class Outline(HTMLParser):
    """Headings, plus the header's .h1/.h2 lookalikes, with their text.

    helpers.Page keeps tags but not their text, and these tests need the text
    to tell the site name apart from the page's own title.
    """

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.items = []  # [tag, class, text] in document order
        self._open = None
        with open(path, encoding="utf-8") as f:
            self.feed(f.read())

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class") or ""
        if tag in HEADINGS or (tag == "p" and {"h1", "h2"} & set(cls.split())):
            self._open = [tag, cls, ""]
            self.items.append(self._open)

    def handle_endtag(self, tag):
        if self._open and tag == self._open[0]:
            self._open[2] = " ".join(self._open[2].split())
            self._open = None

    def handle_data(self, data):
        if self._open:
            self._open[2] += data

    def text_of(self, tag):
        return [text for t, _, text in self.items if t == tag]


def outline(page):
    return Outline(page.path)


class TestHeadings(SiteTestCase):
    def test_every_page_has_exactly_one_h1(self):
        for page in pages():
            with self.subTest(page=page.url):
                self.assertEqual(len(page.find("h1")), 1)

    def test_nothing_outranks_the_h1(self):
        for page in pages():
            with self.subTest(page=page.url):
                first_heading = next(t for t, _ in page.tags if t in HEADINGS)
                self.assertEqual(first_heading, "h1")

    def test_home_h1_is_the_site_name(self):
        home = outline(next(p for p in pages() if p.url == "/"))
        self.assertEqual(home.text_of("h1"), [SITE_NAME])
        self.assertEqual(home.text_of("h2")[:1], [TAGLINE])

    def test_site_name_is_not_a_heading_off_the_home_page(self):
        for page in pages():
            if page.url == "/":
                continue
            with self.subTest(page=page.url):
                o = outline(page)
                headings = [text for t, _, text in o.items if t in HEADINGS]
                self.assertNotIn(SITE_NAME, headings)
                self.assertNotIn(TAGLINE, headings)

    def test_site_name_keeps_its_heading_look_off_the_home_page(self):
        # Bootstrap's .h1/.h2 plus the "header .h1" rules are what keep the
        # <p> versions looking like the old headings; losing a class is a
        # silent visual regression the outline tests above cannot see.
        for page in pages():
            if page.url == "/":
                continue
            with self.subTest(page=page.url):
                lookalikes = [(cls.split(), text) for t, cls, text in outline(page).items if t == "p"]
                self.assertEqual(
                    lookalikes,
                    [(["h1"], SITE_NAME), (["h2", "hidden-xs"], TAGLINE)],
                )

    def test_post_h1_is_the_post_title(self):
        for page in articles():
            with self.subTest(page=page.url):
                expected = page.title.removesuffix(" - Randall Degges").strip()
                self.assertEqual(outline(page).text_of("h1"), [expected])

    def test_404_h1_is_its_own(self):
        # The site name isn't a heading off the home page, so the 404 page
        # needs its own or it has no heading at all.
        page = next(p for p in pages() if p.url == "/404.html")
        [h1] = outline(page).text_of("h1")
        self.assertTrue(h1)
        self.assertNotEqual(h1, SITE_NAME)


if __name__ == "__main__":
    unittest.main()
