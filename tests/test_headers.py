"""The Cloudflare _headers file is published, well formed, and matches render.yaml."""

import glob
import os
import re
import unittest

from helpers import PUBLIC, SiteTestCase

HEADERS = os.path.join(PUBLIC, "_headers")
RENDER_YAML = os.path.join(os.path.dirname(__file__), "..", "render.yaml")

# One render.yaml header entry. The value is either on the same line or a
# folded ">-" block: lines indented deeper than "value:", joined with spaces.
RENDER_RULE = re.compile(
    r"^[ ]*- path: (?P<path>\S+)\n"
    r"[ ]*name: (?P<name>.+)\n"
    r"(?P<indent>[ ]*)value: (?:>-\n(?P<folded>(?:(?P=indent)[ ]+\S.*\n?)+)|(?P<value>.+))",
    re.M,
)


def normalize(value):
    return " ".join(value.split())


def header_lines():
    """(line number, line) for every non-blank, non-comment line of public/_headers."""
    with open(HEADERS, encoding="utf-8") as f:
        return [(n, line.rstrip("\n")) for n, line in enumerate(f, 1) if line.strip() and not line.lstrip().startswith("#")]


def parse_headers():
    """{pattern: {header-name-lowercased: value}} from public/_headers."""
    rules, current = {}, None
    for _, line in header_lines():
        if not line[0].isspace():
            current = rules.setdefault(line.strip(), {})
        else:
            name, _, value = line.strip().partition(":")
            current[name.strip().lower()] = value.strip()
    return rules


def render_triples():
    """{(path, header-name-lowercased, value)} from render.yaml."""
    with open(RENDER_YAML, encoding="utf-8") as f:
        text = f.read()
    matches = list(RENDER_RULE.finditer(text))
    # Every "path:" must belong to a parsed rule, so a rule written in a shape
    # the regex does not know fails here instead of dropping out of the sync.
    paths = re.findall(r"^[ ]*- path:", text, re.M)
    if len(matches) != len(paths):
        raise AssertionError(f"parsed {len(matches)} of {len(paths)} render.yaml header rules")
    return {(m["path"], m["name"].strip().lower(), normalize(m["folded"] or m["value"])) for m in matches}


class TestHeaders(SiteTestCase):
    def setUp(self):
        self.rules = parse_headers()

    def test_security_headers_apply_to_everything(self):
        every = self.rules["/*"]
        self.assertIn("max-age=63072000", every["strict-transport-security"])
        self.assertEqual(every["x-content-type-options"], "nosniff")
        self.assertIn("frame-ancestors 'none'", every["content-security-policy"])
        self.assertIn("object-src 'none'", every["content-security-policy"])

    def test_csp_forbids_script_and_inline_style(self):
        csp = dict(
            (d.split()[0], d.split()[1:])
            for d in self.rules["/*"]["content-security-policy"].split(";")
            if d.strip()
        )
        self.assertEqual(csp["default-src"], ["'none'"])
        self.assertEqual(csp["script-src"], ["'none'"])
        self.assertNotIn("'unsafe-inline'", csp["style-src"])
        self.assertIn("https://buttondown.com", csp["form-action"])

    def test_deprecated_headers_are_gone(self):
        # X-XSS-Protection is ignored by current browsers and could open
        # holes in old ones; interest-cohort was Google's abandoned FLoC.
        every = self.rules["/*"]
        self.assertNotIn("x-xss-protection", every)
        self.assertNotIn("interest-cohort", every["permissions-policy"])

    def test_fingerprinted_assets_are_cached_forever(self):
        self.assertIn("immutable", self.rules["/static/*"]["cache-control"])

    def test_text_files_name_their_charset(self):
        self.assertEqual(self.rules["/.well-known/security.txt"]["content-type"], "text/plain; charset=utf-8")
        self.assertEqual(self.rules["/llms.txt"]["content-type"], "text/plain; charset=utf-8")
        self.assertEqual(self.rules["/*/index.md"]["content-type"], "text/markdown; charset=utf-8")
        # A rule for a file the build no longer writes would do nothing.
        self.assertTrue(os.path.isfile(os.path.join(PUBLIC, ".well-known", "security.txt")))
        self.assertTrue(os.path.isfile(os.path.join(PUBLIC, "llms.txt")))
        self.assertTrue(glob.glob(os.path.join(PUBLIC, "*", "*", "index.md")))

    def test_header_lines_are_within_cloudflare_limits(self):
        # Cloudflare ignores the file past 100 rules and lines past 2,000
        # characters, silently.
        self.assertLessEqual(len(self.rules), 100)
        with open(HEADERS, encoding="utf-8") as f:
            for line in f:
                self.assertLessEqual(len(line), 2000)

    def test_file_is_structurally_valid(self):
        # Not a full parser: this catches the structural failures we know
        # about. A header line with no pattern above it or no colon, and a
        # pattern with more than one splat, are each dropped by Cloudflare
        # without an error.
        pattern = None
        for n, line in header_lines():
            if not line[0].isspace():
                pattern = line.strip()
                self.assertLessEqual(pattern.count("*"), 1, f"line {n}: more than one splat")
            else:
                self.assertIsNotNone(pattern, f"line {n}: header line with no pattern above it")
                self.assertIn(":", line, f"line {n}: header line with no colon")

    def test_matches_render_yaml(self):
        # Render serves production from render.yaml; Cloudflare will serve it
        # from _headers. Both must send the same headers, except Content-Type,
        # which only Cloudflare sets.
        render = render_triples()
        cloudflare = {
            (pattern, name, normalize(value))
            for pattern, headers in self.rules.items()
            for name, value in headers.items()
            if name != "content-type"
        }
        # Fail closed: a parser that finds nothing would make the sets equal.
        self.assertGreaterEqual(len(render), 2)
        self.assertGreaterEqual(len(cloudflare), 2)
        self.assertEqual(render, cloudflare)

    def test_render_yaml_sets_no_content_type(self):
        self.assertNotIn("content-type", {name for _, name, _ in render_triples()})


if __name__ == "__main__":
    unittest.main()
