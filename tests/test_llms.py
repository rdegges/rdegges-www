"""AI-readable versions of the site: /llms.txt and a Markdown copy of each post."""

import glob
import os
import re
import unittest
from urllib.parse import unquote, urljoin, urlparse

from helpers import PUBLIC, SiteTestCase, articles, pages, public_file

SITE = "https://rdegges.com"
CONTENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "content"))

# One llms.txt post entry: "- [Title](https://rdegges.com/YYYY/slug/index.md) (YYYY-MM-DD)"
# with an optional ": description". Anything else under ## Posts means a title
# or description broke the line (a "]", a newline) and the list is malformed.
ENTRY = re.compile(
    r"- \[(?P<title>[^\[\]\n]+)\]\((?P<url>https://rdegges\.com/\d{4}/[^/()\s]+/index\.md)\)"
    r" \((?P<date>\d{4}-\d{2}-\d{2})\)(?:: (?P<desc>.+))?"
)

# Markdown link and image destinations: inline "](dest" and reference
# definitions "[label]: dest" at the start of a line.
INLINE_DEST = re.compile(r"\]\(\s*<?([^)\s>]+)")
REF_DEST = re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)", re.M)

# Hugo template and shortcode delimiters. A reader of the .md file gets the
# raw source, so any of these would be served as literal text.
TEMPLATE_SYNTAX = re.compile(r"\{\{[<%]|[>%]\}\}")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def markdown_copies():
    """(post url, built index.md path) for every post."""
    return [(page.url, os.path.join(PUBLIC, page.url.lstrip("/"), "index.md")) for page in articles()]


def source_bodies():
    """Post URL -> its content file's body, front matter removed."""
    bodies = {}
    for path in glob.glob(os.path.join(CONTENT, "*", "*", "index.md")):
        text = read(path)
        _, front, body = text.split("---\n", 2)
        slug = re.search(r'^slug:\s*"?([^"\n]+)"?\s*$', front, re.M).group(1)
        section = os.path.basename(os.path.dirname(os.path.dirname(path)))
        bodies[f"/{section}/{slug}/"] = body
    return bodies


class TestLlmsTxt(SiteTestCase):
    def setUp(self):
        self.text = read(os.path.join(PUBLIC, "llms.txt"))
        self.posts_section = self.text.split("\n## Posts\n", 1)[1]

    def test_follows_the_llmstxt_shape(self):
        # https://llmstxt.org: an H1 name, then a blockquote summary.
        lines = self.text.splitlines()
        self.assertEqual(lines[0], "# Randall Degges")
        self.assertTrue(next(l for l in lines[1:] if l).startswith("> "))
        self.assertIn("\n## Posts\n", self.text)

    def test_every_line_under_posts_is_one_well_formed_entry(self):
        bad = [l for l in self.posts_section.splitlines() if l and not ENTRY.fullmatch(l)]
        self.assertEqual(bad, [], "malformed llms.txt entries")

    def test_lists_exactly_the_posts_once_each(self):
        urls = [m["url"] for m in ENTRY.finditer(self.posts_section)]
        self.assertEqual(len(set(urls)), len(urls), "a post is listed twice")
        self.assertEqual(
            sorted(u.removeprefix(SITE).removesuffix("index.md") for u in urls),
            sorted(p.url for p in articles()),
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(os.path.isfile(public_file(url.removeprefix(SITE))))

    def test_entry_title_and_date_match_the_post(self):
        by_url = {p.url: p for p in articles()}
        for m in ENTRY.finditer(self.posts_section):
            page = by_url[m["url"].removeprefix(SITE).removesuffix("index.md")]
            with self.subTest(page=page.url):
                self.assertEqual(m["title"], page.meta("og:title"))
                self.assertEqual(m["date"], page.meta("article:published_time")[:10])
                self.assertEqual(m["desc"], page.meta("description") or None)

    def test_is_plain_text_not_html_escaped(self):
        # isPlainText renders with text/template; an html/template regression
        # would turn "I'm" into "I&#39;m" for every reader.
        self.assertIn("I'm Writing Again", self.text)
        self.assertNotRegex(self.text, r"&(#\d+|#x[0-9a-fA-F]+|amp|lt|gt|quot);")

    def test_contact_links_are_absolute(self):
        for label in ("Website", "Feed"):
            with self.subTest(label=label):
                line = re.search(rf"^- {label}: (\S+)$", self.text, re.M)
                self.assertIsNotNone(line, label)
                self.assertTrue(line.group(1).startswith(SITE + "/"), line.group(1))


class TestMarkdownAlternates(SiteTestCase):
    def test_every_post_links_its_markdown_version(self):
        for page in articles():
            with self.subTest(page=page.url):
                alts = page.find("link", rel="alternate", type="text/markdown")
                self.assertEqual(len(alts), 1)
                self.assertEqual(alts[0]["href"], page.url + "index.md")
                path = public_file(alts[0]["href"])
                with open(path, encoding="utf-8") as f:
                    first = f.readline().strip()
                self.assertTrue(first.startswith("# "), path)
                self.assertGreater(os.path.getsize(path), 200, "suspiciously empty")

    def test_only_posts_advertise_a_markdown_version(self):
        posts = {p.url for p in articles()}
        for page in pages():
            if page.url in posts:
                continue
            with self.subTest(page=page.url):
                self.assertEqual(page.find("link", type="text/markdown"), [])
        self.assertFalse(os.path.exists(os.path.join(PUBLIC, "index.md")))


class TestMarkdownCopies(SiteTestCase):
    def test_header_cites_title_author_date_and_canonical_url(self):
        for page in articles():
            with self.subTest(page=page.url):
                lines = read(os.path.join(PUBLIC, page.url.lstrip("/"), "index.md")).splitlines()
                self.assertEqual(lines[0], "# " + page.meta("og:title"))
                byline = lines[2].split(" · ")
                self.assertEqual(byline[0], "By Randall Degges")
                self.assertEqual(byline[2], page.find("link", rel="canonical")[0]["href"])

    def test_carries_the_full_post_text(self):
        # Every source line that is plain Markdown must reach the copy. Lines
        # holding template syntax are left out: how they render is up to the
        # template, not this test.
        bodies = source_bodies()
        for url, path in markdown_copies():
            with self.subTest(page=url):
                copy = read(path)
                missing = [
                    l for l in bodies[url].splitlines()
                    if l.strip() and not TEMPLATE_SYNTAX.search(l) and l not in copy
                ]
                self.assertEqual(missing, [])

    def test_no_unrendered_hugo_shortcodes(self):
        # Served as-is, {{< relref "..." >}} is a dead link to a reader or model.
        leaks = []
        for url, path in markdown_copies():
            for n, line in enumerate(read(path).splitlines(), 1):
                if TEMPLATE_SYNTAX.search(line):
                    leaks.append(f"{url}index.md:{n}: {line.strip()}")
        self.assertEqual(leaks, [], f"{len(leaks)} unrendered shortcodes:\n" + "\n".join(leaks))

    def test_local_links_and_images_resolve(self):
        # The template keeps references relative, so they must resolve
        # against the .md file's own URL, the same as in the HTML.
        broken = []
        for url, path in markdown_copies():
            text = read(path)
            base = SITE + url + "index.md"
            for ref in INLINE_DEST.findall(text) + REF_DEST.findall(text):
                target = urlparse(urljoin(base, ref))
                if target.scheme not in ("http", "https") or target.netloc != "rdegges.com":
                    continue
                if not os.path.exists(public_file(unquote(target.path))):
                    broken.append(f"{url}index.md: {ref}")
        self.assertEqual(broken, [], f"{len(broken)} broken references:\n" + "\n".join(broken))


if __name__ == "__main__":
    unittest.main()
