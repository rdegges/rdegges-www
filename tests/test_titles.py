"""Page titles lead with what's on the page and end with the site name."""

import unittest
from collections import Counter

from helpers import SiteTestCase, articles, pages


class TestTitles(SiteTestCase):
    def test_home_title(self):
        home = next(p for p in pages() if p.url == "/")
        self.assertEqual(home.title, "Randall Degges - Random Thoughts of a Happy Programmer")

    def test_post_titles_lead_with_the_post(self):
        for page in articles():
            with self.subTest(page=page.url):
                self.assertTrue(page.title.endswith(" - Randall Degges"), page.title)
                self.assertFalse(page.title.startswith("Randall Degges - "), page.title)

    def test_titles_are_unique(self):
        dupes = [t for t, n in Counter(p.title for p in pages()).items() if n > 1]
        self.assertEqual(dupes, [])


if __name__ == "__main__":
    unittest.main()
