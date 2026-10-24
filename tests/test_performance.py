"""Budgets for what every page makes the browser download before it renders."""

import os
import re
import unittest

from helpers import PUBLIC, SiteTestCase, pages, public_file

# The stylesheet blocks rendering on every page. It was 146 KB when it was a
# full Bootstrap theme; pruned it is about 26 KB. The budget leaves room to
# grow without letting a whole framework back in unnoticed.
CSS_BUDGET = 40_000


class TestStylesheet(SiteTestCase):
    def stylesheets(self):
        hrefs = {a["href"] for p in pages() for a in p.find("link", rel="stylesheet")}
        self.assertTrue(hrefs, "no stylesheet found")
        return hrefs

    def test_one_stylesheet_site_wide(self):
        self.assertEqual(len(self.stylesheets()), 1)

    def test_stylesheet_fits_the_budget(self):
        for href in self.stylesheets():
            size = os.path.getsize(public_file(href))
            self.assertLessEqual(size, CSS_BUDGET, f"{href} is {size:,} bytes")

    def test_stylesheet_makes_no_third_party_requests(self):
        for href in self.stylesheets():
            css = open(public_file(href), encoding="utf-8").read()
            self.assertNotIn("@import", css)
            for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", css):
                self.assertFalse(re.match(r"(https?:)?//", url), url)
                if not url.startswith("data:"):
                    self.assertTrue(os.path.exists(public_file(url)), f"missing {url}")


if __name__ == "__main__":
    unittest.main()
