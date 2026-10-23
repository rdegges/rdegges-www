"""Shared helpers for the tests in this directory.

The tests check the built site, not the templates: they read ./public, so
run a build first (`make build`, or ./scripts/*build.sh in CI). Each test
file covers one concern so it can land with the change it guards.

Only the standard library is used, so CI needs nothing but Python.
"""

import os
import unittest
from html.parser import HTMLParser

PUBLIC = os.path.abspath(
    os.environ.get("SITE_DIR", os.path.join(os.path.dirname(__file__), "..", "public"))
)


class Page(HTMLParser):
    """The parts of an HTML document the tests look at."""

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.url = "/" + os.path.relpath(path, PUBLIC).replace(os.sep, "/")
        self.url = self.url.removesuffix("index.html")
        self.tags = []  # (tag, attrs) in document order
        self.title = ""
        self.scripts = []  # (attrs, text)
        self._in = None
        with open(path, encoding="utf-8") as f:
            self.feed(f.read())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag in ("title", "script"):
            self._in = (tag, attrs)
            if tag == "script":
                self.scripts.append((attrs, ""))

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, data):
        if not self._in:
            return
        tag, attrs = self._in
        if tag == "title":
            self.title += data
        else:
            self.scripts[-1] = (attrs, self.scripts[-1][1] + data)

    def find(self, tag, **attrs):
        """Every element named tag whose attributes include attrs."""
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]

    def meta(self, key):
        """content of <meta name=key> or <meta property=key>, or None."""
        for a in self.find("meta"):
            if key in (a.get("name"), a.get("property")):
                return a.get("content")
        return None

    @property
    def is_alias(self):
        """Hugo writes a meta-refresh stub for every alias."""
        return any(a.get("http-equiv") == "refresh" for a in self.find("meta"))


def public_file(url):
    """The file a URL path resolves to under PUBLIC (directories -> index.html)."""
    path = os.path.join(PUBLIC, url.split("#")[0].split("?")[0].lstrip("/"))
    if os.path.isdir(path):
        path = os.path.join(path, "index.html")
    return path


def pages(include_aliases=False):
    """Every built HTML page, parsed once and cached."""
    if not hasattr(pages, "_cache"):
        found = []
        for root, _, files in os.walk(PUBLIC):
            for name in files:
                if name.endswith(".html"):
                    found.append(Page(os.path.join(root, name)))
        pages._cache = sorted(found, key=lambda p: p.url)
    return [p for p in pages._cache if include_aliases or not p.is_alias]


def articles():
    """Pages for individual posts: /YYYY/slug/."""
    return [p for p in pages() if p.url[1:5].isdigit()]


class SiteTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(os.path.join(PUBLIC, "index.html")):
            # Fail rather than skip: a CI run where the build silently
            # produced nothing must not pass by testing nothing.
            raise FileNotFoundError(f"no built site at {PUBLIC}; run a build first")
