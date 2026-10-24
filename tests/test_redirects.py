"""_redirects gives every moved URL a real 301 to a page that exists."""

import os
import unittest

from helpers import PUBLIC, Page, SiteTestCase, pages, public_file

OLD_FEEDS = {"/feeds/atom.xml", "/index.xml"}


def rules():
    with open(os.path.join(PUBLIC, "_redirects"), encoding="utf-8") as f:
        return [l.split() for l in f if l.strip() and not l.startswith("#")]


class TestRedirects(SiteTestCase):
    def test_rules_are_well_formed_and_within_cloudflare_limits(self):
        # https://developers.cloudflare.com/workers/platform/limits/#static-assets:
        # 2,000 static rules, 1,000 characters per rule. Past either limit
        # Cloudflare drops rules instead of failing the deploy.
        all_rules = rules()
        self.assertLessEqual(len(all_rules), 2000)
        sources = [r[0] for r in all_rules]
        self.assertEqual(len(sources), len(set(sources)), "duplicate source")
        for rule in all_rules:
            with self.subTest(rule=rule):
                self.assertEqual(len(rule), 3)
                self.assertEqual(rule[2], "301")
                self.assertLessEqual(len(" ".join(rule)), 1000)
                # A splat or placeholder makes a rule dynamic, which has
                # its own limit of 100.
                self.assertNotRegex(rule[0], r"[*:]", "dynamic rule")

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

    def test_old_feed_urls_redirect_to_the_feed(self):
        table = dict((s, d) for s, d, _ in rules())
        for source in sorted(OLD_FEEDS):
            with self.subTest(source=source):
                self.assertEqual(table.get(source), "/feed.xml")

    def test_sources_and_destinations_are_site_paths(self):
        # Cloudflare matches the source against the request path, so a rule
        # without a leading slash never fires. A destination with a scheme
        # or a protocol-relative "//" would send visitors off the site.
        for source, dest, _ in rules():
            with self.subTest(source=source):
                for path in (source, dest):
                    self.assertTrue(path.startswith("/"), path)
                    self.assertFalse(path.startswith("//"), path)
                    self.assertNotIn("://", path)

    def test_no_rule_shadows_real_content(self):
        # Cloudflare applies a redirect even where a file exists, so a rule
        # whose source is a real page or asset would hide it. A source may
        # only be missing from the build or be one of Hugo's alias stubs.
        for source, _, _ in rules():
            with self.subTest(source=source):
                path = public_file(source)
                if not os.path.isfile(path):
                    continue
                self.assertTrue(path.endswith(".html") and Page(path).is_alias, path)

    def test_every_rule_comes_from_an_alias_or_an_old_feed(self):
        # The file is generated from aliases; a rule with neither origin is
        # a stray that nothing else in the build accounts for.
        stubs = {p.url.rstrip("/") for p in pages(include_aliases=True) if p.is_alias}
        for source, _, _ in rules():
            with self.subTest(source=source):
                self.assertTrue(source in OLD_FEEDS or source.rstrip("/") in stubs, source)

    def test_no_redirect_chains(self):
        # One hop: a destination that is itself a source costs a second 301.
        all_rules = rules()
        sources = {s for s, _, _ in all_rules}
        for source, dest, _ in all_rules:
            with self.subTest(source=source):
                self.assertNotIn(dest, sources)
                self.assertNotIn(dest.rstrip("/"), sources)


if __name__ == "__main__":
    unittest.main()
