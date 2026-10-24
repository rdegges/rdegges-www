"""Every page describes itself and its author as schema.org JSON-LD."""

import json
import os
import unittest
from datetime import datetime
from urllib.parse import urlparse

from helpers import SiteTestCase, articles, pages, public_file

HOME = "https://rdegges.com/"
PERSON = HOME + "#person"
WEBSITE = HOME + "#website"


def blocks(page):
    return [text for attrs, text in page.scripts if attrs.get("type") == "application/ld+json"]


def graph(page):
    found = blocks(page)
    if not found:
        return {}
    data = json.loads(found[0])
    return {node["@id"]: node for node in data["@graph"]}


def references(value):
    """Every {"@id": ...} reference nested anywhere in value."""
    if isinstance(value, dict):
        if set(value) == {"@id"}:
            yield value["@id"]
        for v in value.values():
            yield from references(v)
    elif isinstance(value, list):
        for v in value:
            yield from references(v)


def home():
    return next(p for p in pages() if p.url == "/")


class TestStructuredData(SiteTestCase):
    def test_one_valid_block_per_page(self):
        for page in pages():
            if page.url == "/404.html":
                continue
            with self.subTest(page=page.url):
                found = blocks(page)
                self.assertEqual(len(found), 1)
                self.assertEqual(json.loads(found[0])["@context"], "https://schema.org")

    def test_404_has_no_structured_data(self):
        page = next(p for p in pages() if p.url == "/404.html")
        self.assertEqual(blocks(page), [])

    def test_text_cannot_close_the_script_element(self):
        # Titles and descriptions are free text. A raw "<" would let a
        # "</script>" in a post title end the block early and spill the rest
        # into the page as HTML; jsonify escapes it as <, and this keeps
        # it that way if the pipe ever changes.
        for page in pages():
            for text in blocks(page):
                with self.subTest(page=page.url):
                    self.assertNotIn("<", text)

    def test_no_value_is_null_or_empty(self):
        # A missing optional field must be left out, not emitted as null or
        # "" -- validators reject both. (Deleting worksForURL from hugo.toml
        # while keeping worksFor currently emits "url": null.)
        def walk(value, path):
            if isinstance(value, dict):
                for k, v in value.items():
                    yield from walk(v, f"{path}.{k}")
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    yield from walk(v, f"{path}[{i}]")
            elif value is None or value == "":
                yield path

        for page in pages():
            for text in blocks(page):
                with self.subTest(page=page.url):
                    self.assertEqual(list(walk(json.loads(text), "$")), [])

    def test_home_describes_the_site_and_its_author(self):
        nodes = graph(home())
        person = nodes[PERSON]
        self.assertEqual(person["@type"], "Person")
        self.assertEqual(person["name"], "Randall Degges")
        self.assertEqual(person["url"], HOME)
        self.assertIn("https://github.com/rdegges", person["sameAs"])
        self.assertEqual(nodes[WEBSITE]["@type"], "WebSite")
        self.assertEqual(nodes[WEBSITE]["url"], HOME)
        # The home page describes the site, not a post.
        self.assertEqual(sorted(n["@type"] for n in nodes.values()), ["Person", "WebSite"])

    def test_profiles_are_distinct_https_urls(self):
        same_as = graph(home())[PERSON]["sameAs"]
        self.assertEqual(len(same_as), len(set(same_as)))
        for url in same_as:
            with self.subTest(url=url):
                parsed = urlparse(url)
                self.assertEqual(parsed.scheme, "https")
                self.assertTrue(parsed.netloc)
                self.assertNotEqual(parsed.netloc, "rdegges.com", "sameAs is for other sites")

    def test_every_page_describes_the_same_person_and_site(self):
        # One entity only works if every page says the same thing about it.
        expected = graph(home())
        for page in pages():
            if page.url == "/404.html":
                continue
            with self.subTest(page=page.url):
                nodes = graph(page)
                self.assertEqual(nodes[PERSON], expected[PERSON])
                self.assertEqual(nodes[WEBSITE], expected[WEBSITE])

    def test_ids_are_unique_and_every_reference_resolves(self):
        for page in pages():
            for text in blocks(page):
                with self.subTest(page=page.url):
                    ids = [node["@id"] for node in json.loads(text)["@graph"]]
                    self.assertEqual(len(ids), len(set(ids)))
                    for ref in references(json.loads(text)["@graph"]):
                        self.assertIn(ref, ids)

    def test_every_post_is_a_blog_posting_by_the_author(self):
        for page in articles():
            with self.subTest(page=page.url):
                nodes = graph(page)
                post = nodes["https://rdegges.com" + page.url + "#article"]
                self.assertEqual(post["@type"], "BlogPosting")
                for field in ("headline", "datePublished", "dateModified", "description"):
                    self.assertTrue(post.get(field), field)
                # Google truncates headlines past 110 characters.
                self.assertLessEqual(len(post["headline"]), 110)
                # The author reference must resolve inside the same page.
                self.assertEqual(nodes[post["author"]["@id"]]["@type"], "Person")
                self.assertEqual(post["author"]["@id"], PERSON)
                self.assertEqual(post["publisher"]["@id"], PERSON)
                self.assertEqual(post["isPartOf"]["@id"], WEBSITE)

    def test_post_agrees_with_the_rest_of_the_page(self):
        # Search engines distrust structured data that contradicts the page,
        # so each field must match the tag that already states it.
        for page in articles():
            with self.subTest(page=page.url):
                post = graph(page)["https://rdegges.com" + page.url + "#article"]
                canonical = page.find("link", rel="canonical")[0]["href"]
                self.assertEqual(post["url"], canonical)
                self.assertEqual(post["mainEntityOfPage"], canonical)
                self.assertEqual(post["headline"], page.meta("og:title"))
                self.assertEqual(post["description"], page.meta("description"))
                if "image" in post:
                    self.assertEqual(post["image"], page.meta("og:image"))
                self.assertEqual(post["datePublished"], page.meta("article:published_time"))
                self.assertEqual(post["dateModified"], page.meta("article:modified_time"))
                tags = [a["content"] for a in page.find("meta") if a.get("property") == "article:tag"]
                self.assertEqual(post.get("keywords", []), tags)
                shown = [a["datetime"] for t, a in page.tags if t == "time" and "datetime" in a]
                self.assertEqual(post["datePublished"][:10], shown[0])

    def test_post_dates_are_iso_8601_with_a_zone(self):
        for page in articles():
            with self.subTest(page=page.url):
                post = graph(page)["https://rdegges.com" + page.url + "#article"]
                published = datetime.fromisoformat(post["datePublished"])
                modified = datetime.fromisoformat(post["dateModified"])
                self.assertIsNotNone(published.tzinfo)
                self.assertIsNotNone(modified.tzinfo)
                self.assertGreaterEqual(modified, published)

    def test_post_image_is_a_built_file(self):
        for page in articles():
            with self.subTest(page=page.url):
                post = graph(page)["https://rdegges.com" + page.url + "#article"]
                if "image" not in post:
                    continue
                url = urlparse(post["image"])
                self.assertEqual((url.scheme, url.netloc), ("https", "rdegges.com"))
                self.assertTrue(os.path.isfile(public_file(url.path)), url.path)

    def test_word_count_is_a_positive_integer(self):
        for page in articles():
            with self.subTest(page=page.url):
                post = graph(page)["https://rdegges.com" + page.url + "#article"]
                self.assertIsInstance(post["wordCount"], int)
                self.assertGreater(post["wordCount"], 0)

    def test_keywords_are_a_list_of_tags(self):
        for page in articles():
            post = graph(page)["https://rdegges.com" + page.url + "#article"]
            if "keywords" not in post:
                continue
            with self.subTest(page=page.url):
                self.assertIsInstance(post["keywords"], list)
                for keyword in post["keywords"]:
                    self.assertIsInstance(keyword, str)
                    self.assertTrue(keyword.strip())

    def test_tags_that_were_strings_become_separate_keywords(self):
        # Regression: these two posts had `tags: "a, b"`, which emitted one
        # comma-joined string instead of a list of tags.
        expected = {
            "/2010/being-myself/": ["personal development"],
            "/2012/how-to-instantly-fix-problematic-deployments-on-heroku/": ["programming", "devops"],
        }
        by_url = {p.url: p for p in articles()}
        for url, keywords in expected.items():
            with self.subTest(page=url):
                post = graph(by_url[url])["https://rdegges.com" + url + "#article"]
                self.assertEqual(post["keywords"], keywords)


if __name__ == "__main__":
    unittest.main()
