"""Every internal link and asset reference on the site resolves.

The render-image hook already fails the build on a missing image in
Markdown; this covers everything else -- links between posts, templates,
srcset candidates, stylesheets, icons -- in the built output, which is what
visitors actually get.
"""

import os
import unittest
from urllib.parse import unquote, urljoin, urlparse

from helpers import SiteTestCase, pages, public_file


def local_refs(page):
    for tag, attrs in page.tags:
        for attr in ("href", "src"):
            if attr in attrs:
                yield tag, attrs[attr]
        for candidate in attrs.get("srcset", "").split(","):
            if candidate.strip():
                yield tag, candidate.split()[0]


class TestLinks(SiteTestCase):
    def test_internal_references_resolve(self):
        broken = []
        for page in pages(include_aliases=True):
            for tag, ref in local_refs(page):
                url = urlparse(urljoin("https://rdegges.com" + page.url, ref))
                if url.scheme not in ("http", "https") or url.netloc not in ("rdegges.com", "www.rdegges.com"):
                    continue
                if not os.path.exists(public_file(unquote(url.path))):
                    broken.append(f"{page.url}: <{tag}> {ref}")
        self.assertEqual(broken, [], "broken internal references:\n" + "\n".join(broken))


if __name__ == "__main__":
    unittest.main()
