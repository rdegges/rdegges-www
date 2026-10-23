"""AI-readable versions of the site: /llms.txt and a Markdown copy of each post."""

import os
import re
import unittest

from helpers import PUBLIC, SiteTestCase, articles, public_file


class TestLlmsTxt(SiteTestCase):
    def setUp(self):
        with open(os.path.join(PUBLIC, "llms.txt"), encoding="utf-8") as f:
            self.text = f.read()

    def test_follows_the_llmstxt_shape(self):
        # https://llmstxt.org: an H1 name, then a blockquote summary.
        lines = self.text.splitlines()
        self.assertEqual(lines[0], "# Randall Degges")
        self.assertTrue(next(l for l in lines[1:] if l).startswith("> "))
        self.assertIn("\n## Posts\n", self.text)

    def test_lists_every_post_once_with_a_working_link(self):
        links = re.findall(r"^- \[[^\]]+\]\((https://rdegges\.com/[^)]+)\)", self.text, re.M)
        self.assertEqual(len(links), len(articles()))
        self.assertEqual(len(set(links)), len(links))
        for url in links:
            with self.subTest(url=url):
                self.assertTrue(os.path.isfile(public_file(url.removeprefix("https://rdegges.com"))))


class TestMarkdownAlternates(SiteTestCase):
    def test_every_post_links_its_markdown_version(self):
        for page in articles():
            with self.subTest(page=page.url):
                alts = page.find("link", rel="alternate", type="text/markdown")
                self.assertEqual(len(alts), 1)
                path = public_file(alts[0]["href"])
                with open(path, encoding="utf-8") as f:
                    first = f.readline().strip()
                self.assertTrue(first.startswith("# "), path)
                self.assertGreater(os.path.getsize(path), 200, "suspiciously empty")


if __name__ == "__main__":
    unittest.main()
