"""robots.txt lets every crawler in and points at the sitemap."""

import os
import unittest

from helpers import PUBLIC, SiteTestCase, public_file


class TestRobots(SiteTestCase):
    def setUp(self):
        with open(os.path.join(PUBLIC, "robots.txt"), encoding="utf-8") as f:
            self.lines = [line.strip() for line in f if line.strip()]

    def test_nothing_is_disallowed(self):
        disallows = [l for l in self.lines if l.lower().startswith("disallow:") and l[9:].strip()]
        self.assertEqual(disallows, [])

    def test_points_at_a_sitemap_that_exists(self):
        sitemaps = [l.split(":", 1)[1].strip() for l in self.lines if l.lower().startswith("sitemap:")]
        self.assertEqual(sitemaps, ["https://rdegges.com/sitemap.xml"])
        self.assertTrue(os.path.isfile(public_file("/sitemap.xml")))


if __name__ == "__main__":
    unittest.main()
