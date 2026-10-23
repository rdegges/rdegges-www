"""_redirects gives every moved URL a real 301 to a page that exists."""

import os
import unittest

from helpers import PUBLIC, SiteTestCase, pages, public_file


def rules():
    with open(os.path.join(PUBLIC, "_redirects"), encoding="utf-8") as f:
        return [l.split() for l in f if l.strip() and not l.startswith("#")]


class TestRedirects(SiteTestCase):
    def test_rules_are_well_formed_and_within_cloudflare_limits(self):
        all_rules = rules()
        self.assertLessEqual(len(all_rules), 2000)
        sources = [r[0] for r in all_rules]
        self.assertEqual(len(sources), len(set(sources)), "duplicate source")
        for rule in all_rules:
            with self.subTest(rule=rule):
                self.assertEqual(len(rule), 3)
                self.assertEqual(rule[2], "301")

    def test_every_destination_exists(self):
        for source, dest, _ in rules():
            with self.subTest(source=source):
                self.assertTrue(os.path.isfile(public_file(dest)), dest)
                self.assertNotEqual(dest.rstrip("/"), source.rstrip("/"), "redirects to itself")

    def test_every_alias_page_has_a_matching_redirect(self):
        table = {source: dest for source, dest, _ in rules()}
        aliases = [p for p in pages(include_aliases=True) if p.is_alias]
        self.assertGreater(len(aliases), 100)
        for page in aliases:
            with self.subTest(alias=page.url):
                target = page.find("link", rel="canonical")[0]["href"].removeprefix("https://rdegges.com")
                self.assertEqual(table.get(page.url), target)
                self.assertEqual(table.get(page.url.rstrip("/")), target)

    def test_old_feed_url_redirects_to_the_feed(self):
        self.assertEqual(dict((s, d) for s, d, _ in rules())["/feeds/atom.xml"], "/feed.xml")


if __name__ == "__main__":
    unittest.main()
