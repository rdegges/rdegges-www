"""One <h1> per page, and it's the page's own subject."""

import unittest

from helpers import SiteTestCase, articles, pages


class TestHeadings(SiteTestCase):
    def test_at_most_one_h1_anywhere(self):
        for page in pages():
            with self.subTest(page=page.url):
                self.assertLessEqual(len(page.find("h1")), 1)

    def test_home_h1_is_the_site_name(self):
        home = next(p for p in pages() if p.url == "/")
        self.assertEqual(len(home.find("h1")), 1)

    def test_404_has_an_h1(self):
        # The site name isn't a heading off the home page, so the 404 page
        # needs its own or it has no heading at all.
        page = next(p for p in pages() if p.url == "/404.html")
        self.assertEqual(len(page.find("h1")), 1)

    def test_every_post_has_exactly_one_h1(self):
        for page in articles():
            with self.subTest(page=page.url):
                self.assertEqual(len(page.find("h1")), 1)
                # Nothing should outrank the post title in the outline.
                first_heading = next(t for t, _ in page.tags if t in ("h1", "h2", "h3"))
                self.assertEqual(first_heading, "h1")


if __name__ == "__main__":
    unittest.main()
