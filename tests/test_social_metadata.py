"""Every page carries a canonical URL and link-preview metadata."""

import os
import unittest
from urllib.parse import urlparse

from helpers import SiteTestCase, articles, pages, public_file


class TestSocialMetadata(SiteTestCase):
    def test_canonical_url_is_the_page_itself(self):
        for page in pages():
            if page.url == "/404.html":
                continue
            with self.subTest(page=page.url):
                links = page.find("link", rel="canonical")
                self.assertEqual(len(links), 1)
                self.assertEqual(links[0]["href"], "https://rdegges.com" + page.url)

    def test_open_graph_basics(self):
        for page in pages():
            with self.subTest(page=page.url):
                for key in ("og:title", "og:description", "og:url", "og:type", "og:image", "twitter:card"):
                    self.assertTrue(page.meta(key), key)

    def test_preview_image_exists_and_has_dimensions(self):
        for page in pages():
            with self.subTest(page=page.url):
                url = urlparse(page.meta("og:image"))
                self.assertEqual(url.netloc, "rdegges.com")
                self.assertTrue(os.path.isfile(public_file(url.path)), url.path)
                self.assertTrue(page.meta("og:image:width") and page.meta("og:image:height"))

    def test_articles_are_typed_and_dated(self):
        for page in articles():
            with self.subTest(page=page.url):
                self.assertEqual(page.meta("og:type"), "article")
                self.assertTrue(page.meta("article:published_time"))
                self.assertEqual(page.meta("twitter:card"), "summary_large_image")


if __name__ == "__main__":
    unittest.main()
