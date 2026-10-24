"""No page runs script or carries inline styles.

The site needs no JavaScript at all, and keeping it that way is what lets
the Content-Security-Policy forbid scripts outright: an injected <script>
then has nothing to run in. Inline styles are kept out for the same reason
on the style-src side. JSON-LD is data, not code, so it is allowed.
"""

import unittest

from helpers import SiteTestCase, pages


class TestNoInlineCode(SiteTestCase):
    def test_no_scripts(self):
        for page in pages(include_aliases=True):
            for attrs, _ in page.scripts:
                with self.subTest(page=page.url):
                    self.assertEqual(attrs.get("type"), "application/ld+json")

    def test_no_event_handler_attributes(self):
        for page in pages(include_aliases=True):
            for tag, attrs in page.tags:
                handlers = [a for a in attrs if a.startswith("on")]
                with self.subTest(page=page.url, tag=tag):
                    self.assertEqual(handlers, [])

    def test_no_inline_styles(self):
        for page in pages(include_aliases=True):
            with self.subTest(page=page.url):
                self.assertEqual([t for t, a in page.tags if "style" in a], [])
                self.assertEqual(page.find("style"), [])


if __name__ == "__main__":
    unittest.main()
