"""The Cloudflare _headers file is published and carries the headers we rely on."""

import os
import unittest

from helpers import PUBLIC, SiteTestCase


def parse_headers():
    """{pattern: {header-name-lowercased: value}} from public/_headers."""
    rules, current = {}, None
    with open(os.path.join(PUBLIC, "_headers"), encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if not line[0].isspace():
                current = rules.setdefault(line.strip(), {})
            else:
                name, _, value = line.strip().partition(":")
                current[name.strip().lower()] = value.strip()
    return rules


class TestHeaders(SiteTestCase):
    def setUp(self):
        self.rules = parse_headers()

    def test_security_headers_apply_to_everything(self):
        every = self.rules["/*"]
        self.assertIn("max-age=63072000", every["strict-transport-security"])
        self.assertEqual(every["x-content-type-options"], "nosniff")
        self.assertIn("frame-ancestors 'none'", every["content-security-policy"])
        self.assertIn("object-src 'none'", every["content-security-policy"])

    def test_fingerprinted_assets_are_cached_forever(self):
        self.assertIn("immutable", self.rules["/static/*"]["cache-control"])

    def test_header_lines_are_within_cloudflare_limits(self):
        # Cloudflare ignores the file past 100 rules and lines past 2,000
        # characters, silently.
        self.assertLessEqual(len(self.rules), 100)
        with open(os.path.join(PUBLIC, "_headers"), encoding="utf-8") as f:
            for line in f:
                self.assertLessEqual(len(line), 2000)


if __name__ == "__main__":
    unittest.main()
