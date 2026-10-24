"""The Content-Security-Policy allows everything the built site loads.

default-src is 'none', so any resource type without its own directive is
blocked, and a browser blocks it silently: the page just renders without
it. These tests read what the built pages and CSS ask for and check each
request against the policy in public/_headers, so a template or content
change that the policy would break fails here instead of on the live site.
"""

import glob
import json
import os
import re
import unittest
from urllib.parse import urlsplit

from helpers import PUBLIC, SiteTestCase, pages
from test_headers import parse_headers

HUGO_TOML = os.path.join(os.path.dirname(__file__), "..", "hugo.toml")


def site_origin():
    with open(HUGO_TOML, encoding="utf-8") as f:
        url = urlsplit(re.search(r'^baseURL\s*=\s*"([^"]+)"', f.read(), re.M)[1])
    return url.scheme, url.hostname


def directives(csp):
    """[(name, [sources])] in policy order, duplicates kept."""
    out = []
    for part in csp.split(";"):
        words = part.split()
        if words:
            out.append((words[0].lower(), words[1:]))
    return out


def policy():
    """{directive: sources}, with each fetch directive falling back to default-src."""
    csp = parse_headers()["/*"]["content-security-policy"]
    found = {}
    for name, sources in directives(csp):
        # A browser uses the first of two same-named directives; keep that.
        found.setdefault(name, sources)
    return found


def effective(found, name):
    return found.get(name, found.get("default-src", ["*"]))


def allows(sources, url):
    """True if a CSP source list admits url, as seen from the site's origin."""
    if "'none'" in sources:
        return False
    parts = urlsplit(url)
    if parts.scheme == "data":
        return "data:" in sources
    origin = site_origin()
    if not parts.netloc:
        return "'self'" in sources
    scheme, host = parts.scheme, parts.hostname
    for source in sources:
        if source == "'self'" and (scheme, host) == origin:
            return True
        if source == "*" or source == f"{scheme}:":
            return True
        if source.startswith("'"):
            continue
        src_scheme, _, src_host = source.rpartition("://")
        src_host = src_host.split("/")[0]
        if src_scheme and src_scheme != scheme:
            continue
        # A host source without a scheme matches http and https.
        if not src_scheme and scheme not in ("http", "https"):
            continue
        if src_host == host or (src_host.startswith("*.") and host.endswith(src_host[1:])):
            return True
    return False


def srcset_urls(value):
    return [c.split()[0] for c in value.split(",") if c.strip()]


class TestCspDirectives(SiteTestCase):
    def test_no_directive_is_repeated(self):
        # A browser obeys the first copy of a directive and ignores the rest,
        # so a repeat added later in the line would do nothing at all.
        csp = parse_headers()["/*"]["content-security-policy"]
        names = [name for name, _ in directives(csp)]
        self.assertGreater(len(names), 1)
        self.assertEqual(len(names), len(set(names)), names)

    def test_allows_matcher_self_check(self):
        # The checks below are only as good as allows(); pin its behavior.
        self.assertTrue(allows(["'self'"], "/static/x.css"))
        self.assertTrue(allows(["'self'"], "https://rdegges.com/x.png"))
        self.assertFalse(allows(["'self'"], "https://evil.example/x.png"))
        self.assertFalse(allows(["'self'"], "data:image/png;base64,AA"))
        self.assertTrue(allows(["'self'", "data:"], "data:image/png;base64,AA"))
        self.assertTrue(allows(["https://buttondown.com"], "https://buttondown.com/api/x"))
        self.assertFalse(allows(["https://buttondown.com"], "http://buttondown.com/api/x"))
        self.assertFalse(allows(["https://buttondown.email"], "https://buttondown.com/api/x"))
        self.assertFalse(allows(["'none'"], "/x"))


class TestCspAllowsTheSite(SiteTestCase):
    def setUp(self):
        self.csp = policy()

    def assert_allowed(self, directive, url, where):
        sources = effective(self.csp, directive)
        self.assertTrue(allows(sources, url), f"{where}: {url} is blocked by {directive} {' '.join(sources)}")

    def test_every_form_posts_where_form_action_allows(self):
        # The subscribe form is the site's only form. If its host is not in
        # form-action, the browser drops the submission with no visible error.
        found = 0
        for page in pages(include_aliases=True):
            for form in page.find("form"):
                found += 1
                with self.subTest(page=page.url):
                    self.assert_allowed("form-action", form.get("action") or page.url, page.url)
        self.assertGreater(found, 0)

    def test_every_html_subresource_is_allowed(self):
        checked = 0
        for page in pages(include_aliases=True):
            for tag, attrs in page.tags:
                rel = (attrs.get("rel") or "").lower().split()
                wanted = []
                if tag == "img":
                    wanted += [("img-src", attrs.get("src"))]
                    wanted += [("img-src", u) for u in srcset_urls(attrs.get("srcset") or "")]
                elif tag == "source":
                    wanted += [("img-src", u) for u in srcset_urls(attrs.get("srcset") or "")]
                elif tag == "link" and "stylesheet" in rel:
                    wanted.append(("style-src", attrs.get("href")))
                elif tag == "link" and "preload" in rel:
                    kind = {"font": "font-src", "style": "style-src", "image": "img-src"}
                    wanted.append((kind.get(attrs.get("as"), "default-src"), attrs.get("href")))
                elif tag == "link" and "manifest" in rel:
                    wanted.append(("manifest-src", attrs.get("href")))
                elif tag == "link" and {"icon", "apple-touch-icon"} & set(rel):
                    wanted.append(("img-src", attrs.get("href")))
                for directive, url in wanted:
                    if url:
                        checked += 1
                        with self.subTest(page=page.url, url=url):
                            self.assert_allowed(directive, url, page.url)
        self.assertGreater(checked, 0)

    def test_no_element_the_policy_blocks_outright(self):
        # default-src 'none' leaves media, frames and objects with nothing
        # to load from, and base-uri 'none' ignores <base>. None of them may
        # appear, or they render as empty boxes or break relative links.
        blocked = ("iframe", "frame", "embed", "object", "video", "audio", "track", "base")
        for page in pages(include_aliases=True):
            with self.subTest(page=page.url):
                self.assertEqual([t for t, _ in page.tags if t in blocked], [])

    def test_every_css_url_is_allowed(self):
        css_files = glob.glob(os.path.join(PUBLIC, "static", "css", "*.css"))
        self.assertTrue(css_files)
        checked = 0
        for path in css_files:
            with open(path, encoding="utf-8") as f:
                css = f.read()
            self.assertNotIn("@import", css, path)
            font_faces = [m.span() for m in re.finditer(r"@font-face\s*{[^}]*}", css)]
            for m in re.finditer(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)", css):
                url = m[2].strip()
                directive = "font-src" if any(a <= m.start() < b for a, b in font_faces) else "img-src"
                checked += 1
                with self.subTest(css=os.path.basename(path), url=url[:60]):
                    self.assert_allowed(directive, url, os.path.basename(path))
        self.assertGreater(checked, 0)

    def test_manifest_icons_are_allowed(self):
        with open(os.path.join(PUBLIC, "site.webmanifest"), encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertTrue(manifest.get("icons"))
        for icon in manifest["icons"]:
            self.assert_allowed("img-src", icon["src"], "site.webmanifest")


if __name__ == "__main__":
    unittest.main()
