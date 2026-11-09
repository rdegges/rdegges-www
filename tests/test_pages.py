"""Baseline invariants every page and feed must keep."""

import os
import unittest
import xml.etree.ElementTree as ET

from helpers import PUBLIC, SiteTestCase, pages, public_file

SITEMAP = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ATOM = "{http://www.w3.org/2005/Atom}"


class TestPages(SiteTestCase):
    def test_every_page_has_a_title_description_and_language(self):
        for page in pages():
            with self.subTest(page=page.url):
                self.assertTrue(page.title.strip(), "empty <title>")
                self.assertTrue(page.meta("description"), "missing meta description")
                self.assertTrue(page.find("html")[0].get("lang"), "missing <html lang>")

    def test_every_image_has_alt_text_attribute(self):
        # alt="" is valid for decorative images; a missing alt is not.
        for page in pages():
            for img in page.find("img"):
                with self.subTest(page=page.url, img=img.get("src")):
                    self.assertIn("alt", img)


class TestSitemap(SiteTestCase):
    def test_every_sitemap_url_exists(self):
        root = ET.parse(os.path.join(PUBLIC, "sitemap.xml")).getroot()
        locs = [loc.text for loc in root.iter(SITEMAP + "loc")]
        self.assertGreater(len(locs), 100)
        for loc in locs:
            with self.subTest(loc=loc):
                self.assertTrue(os.path.isfile(public_file(loc.removeprefix("https://rdegges.com"))))


    def test_every_page_is_in_the_sitemap(self):
        # A page that is built but missing here is one crawlers can only find
        # by following links. About was, because it hid itself from Hugo's
        # page collections; this catches the next page that does.
        root = ET.parse(os.path.join(PUBLIC, "sitemap.xml")).getroot()
        locs = {loc.text for loc in root.iter(SITEMAP + "loc")}
        for page in pages():
            if page.url == "/404.html":
                continue
            with self.subTest(page=page.url):
                self.assertIn("https://rdegges.com" + page.url, locs)


class TestFeed(SiteTestCase):
    def test_feed_is_well_formed_atom_with_entries(self):
        root = ET.parse(os.path.join(PUBLIC, "feed.xml")).getroot()
        self.assertEqual(root.tag, ATOM + "feed")
        entries = root.findall(ATOM + "entry")
        self.assertEqual(len(entries), 20)
        for entry in entries:
            for field in ("id", "title", "updated", "content"):
                self.assertIsNotNone(entry.find(ATOM + field), field)


if __name__ == "__main__":
    unittest.main()
