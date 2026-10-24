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


# The media type a Content-Type rule may give each file extension. Spelled
# out rather than read from mimetypes, whose table depends on the host's
# /etc/mime.types.
MEDIA_TYPES = {".txt": "text/plain", ".md": "text/markdown"}


def raw_rules():
    """[(pattern, [(line number, header-name-lowercased, value)])] in file order.

    Unlike parse_headers, this keeps repeated patterns and repeated names,
    because Cloudflare does not collapse them: it joins the values.
    """
    rules = []
    for n, line in header_lines():
        if not line[0].isspace():
            rules.append((line.strip(), []))
        elif rules:
            name, _, value = line.strip().partition(":")
            rules[-1][1].append((n, name.strip().lower(), value.strip()))
    return rules


def built_urls():
    """Every URL path the built site serves a file at."""
    urls = set()
    for root, _, files in os.walk(PUBLIC):
        for name in files:
            url = "/" + os.path.relpath(os.path.join(root, name), PUBLIC).replace(os.sep, "/")
            urls.add(url)
            if name == "index.html":
                urls.add(url.removesuffix("index.html"))
    urls.discard("/_headers")
    return urls


def matcher(pattern):
    """A regex for a _headers URL pattern. The splat matches anything, slashes included."""
    return re.compile("".join(".*" if part == "*" else re.escape(part) for part in re.split(r"(\*)", pattern)) + r"\Z")


def render_triples(text=None):
    """{(path, header-name-lowercased, value)} from render.yaml, or from text."""
    if text is None:
        with open(RENDER_YAML, encoding="utf-8") as f:
            text = f.read()
    matches = list(RENDER_RULE.finditer(text))
    # Every list item under "headers:" must be a parsed rule, so a rule
    # written in a shape or key order the regex does not know fails here
    # instead of dropping out of the sync.
    headers = re.search(r"^[ ]*headers:.*$", text, re.M)
    items = re.findall(r"^[ ]*- ", text[headers.end():], re.M) if headers else []
    if len(matches) != len(items):
        raise AssertionError(f"parsed {len(matches)} of {len(items)} render.yaml header rules")
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
        # Checked on the raw text too, so it holds even if the parser misses a rule.
        with open(RENDER_YAML, encoding="utf-8") as f:
            text = f.read()
        self.assertIsNone(re.search(r"^[ ]*(?:- )?name:[ ]*Content-Type[ ]*$", text, re.I | re.M))

    def test_render_yaml_parser_rejects_unknown_key_order(self):
        with open(RENDER_YAML, encoding="utf-8") as f:
            text = f.read()
        text = text.rstrip("\n") + "\n      - name: X-Test\n        path: /*\n        value: y\n"
        with self.assertRaises(AssertionError):
            render_triples(text)

    def test_no_url_gets_the_same_header_twice(self):
        # Cloudflare applies every pattern that matches a URL and joins the
        # values of a repeated header with a comma. "DENY, SAMEORIGIN" is not a
        # valid X-Frame-Options, so the browser drops it. parse_headers keeps
        # only the last value per name, so test_matches_render_yaml cannot see
        # this.
        urls = built_urls()
        self.assertGreater(len(urls), 1)
        for url in urls:
            seen = {}
            for pattern, headers in raw_rules():
                if not matcher(pattern).match(url):
                    continue
                for n, name, _ in headers:
                    self.assertNotIn(name, seen, f"{url}: {name} set on line {seen.get(name)} and line {n}")
                    seen[name] = n

    def test_content_type_rules_agree_with_the_files_they_match(self):
        # A Content-Type rule replaces the type Cloudflare would infer, so a
        # broad pattern (/* or /static/*) would mislabel every file under it.
        urls = built_urls()
        found = 0
        for pattern, headers in raw_rules():
            for n, name, value in headers:
                if name != "content-type":
                    continue
                found += 1
                media_type = value.split(";")[0].strip()
                matched = [u for u in urls if matcher(pattern).match(u)]
                self.assertTrue(matched, f"line {n}: {pattern} matches no built file")
                for url in matched:
                    self.assertEqual(MEDIA_TYPES.get(os.path.splitext(url)[1]), media_type, f"line {n}: {pattern} labels {url}")
        self.assertGreaterEqual(found, 1)

    def test_every_pattern_matches_a_built_file(self):
        # A rule for a path the build never writes does nothing, silently.
        urls = built_urls()
        for pattern, _ in raw_rules():
            self.assertTrue(any(matcher(pattern).match(u) for u in urls), f"{pattern} matches no built file")


if __name__ == "__main__":
    unittest.main()
