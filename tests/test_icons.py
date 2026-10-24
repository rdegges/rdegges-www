"""Icons live where browsers look for them, and every page links them."""

import json
import os
import unittest

from helpers import PUBLIC, SiteTestCase, pages, public_file


class TestIcons(SiteTestCase):
    def test_default_locations_exist(self):
        # Browsers fetch these two paths whether or not a page links them,
        # so a missing file is a 404 on every first visit.
        for name in ("favicon.ico", "apple-touch-icon.png"):
            self.assertTrue(os.path.isfile(os.path.join(PUBLIC, name)), name)

    def test_manifest_is_valid_and_its_icons_exist(self):
        with open(os.path.join(PUBLIC, "site.webmanifest"), encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest["name"], "Randall Degges")
        self.assertTrue(manifest["icons"])
        for icon in manifest["icons"]:
            self.assertTrue(os.path.isfile(public_file(icon["src"])), icon["src"])

    def test_every_page_links_its_icons(self):
        for page in pages():
            with self.subTest(page=page.url):
                self.assertTrue(page.find("link", rel="icon"))
                self.assertTrue(page.find("link", rel="apple-touch-icon"))
                self.assertTrue(page.find("link", rel="manifest"))


if __name__ == "__main__":
    unittest.main()
