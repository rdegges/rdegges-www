"""Every page describes itself and its author as schema.org JSON-LD."""

import json
import unittest

from helpers import SiteTestCase, articles, pages


def graph(page):
    blocks = [text for attrs, text in page.scripts if attrs.get("type") == "application/ld+json"]
    if not blocks:
        return {}
    data = json.loads(blocks[0])
    return {node["@id"]: node for node in data["@graph"]}


class TestStructuredData(SiteTestCase):
    def test_one_valid_block_per_page(self):
        for page in pages():
            if page.url == "/404.html":
                continue
            with self.subTest(page=page.url):
                blocks = [t for a, t in page.scripts if a.get("type") == "application/ld+json"]
                self.assertEqual(len(blocks), 1)
                self.assertEqual(json.loads(blocks[0])["@context"], "https://schema.org")

    def test_home_describes_the_site_and_its_author(self):
        nodes = graph(next(p for p in pages() if p.url == "/"))
        person = nodes["https://rdegges.com/#person"]
        self.assertEqual(person["@type"], "Person")
        self.assertEqual(person["name"], "Randall Degges")
        self.assertIn("https://github.com/rdegges", person["sameAs"])
        self.assertEqual(nodes["https://rdegges.com/#website"]["@type"], "WebSite")

    def test_every_post_is_a_blog_posting_by_the_author(self):
        for page in articles():
            with self.subTest(page=page.url):
                nodes = graph(page)
                post = nodes["https://rdegges.com" + page.url + "#article"]
                self.assertEqual(post["@type"], "BlogPosting")
                for field in ("headline", "datePublished", "dateModified", "image", "description"):
                    self.assertTrue(post.get(field), field)
                # Google truncates headlines past 110 characters.
                self.assertLessEqual(len(post["headline"]), 110)
                # The author reference must resolve inside the same page.
                self.assertEqual(nodes[post["author"]["@id"]]["@type"], "Person")


if __name__ == "__main__":
    unittest.main()
