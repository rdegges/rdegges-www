"""Images reserve their space, stay small, and wear a print mat in articles."""

import os
import unittest
from html.parser import HTMLParser

from helpers import SiteTestCase, articles, pages, public_file

# Tags HTMLParser never emits an end event for. Pushing them would make
# every later element look nested inside the image.
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}


class ImageParents(HTMLParser):
    """(img attrs, ancestor (tag, attrs) pairs) for each img, outer first."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append((attrs, list(self.stack)))
        if tag not in VOID:
            self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


def images_in(page):
    parser = ImageParents()
    with open(page.path, encoding="utf-8") as f:
        parser.feed(f.read())
    return parser.images


def classes(attrs):
    return set((attrs.get("class") or "").split())


def mat_kind(ancestors):
    """'full' or 'mat' when the img's parent is that wrapper, else None."""
    if not ancestors:
        return None
    tag, attrs = ancestors[-1]
    kind = classes(attrs)
    if tag == "a" and "img-full" in kind:
        return "full"
    if tag == "span" and "img-mat" in kind:
        return "mat"
    return None


class TestImages(SiteTestCase):
    def test_every_image_declares_its_size(self):
        # width/height let the browser reserve the box before the file
        # arrives, which is what keeps layout shift at zero.
        for page in pages():
            for img in page.find("img"):
                with self.subTest(page=page.url, img=img.get("src")):
                    self.assertTrue(img.get("width") and img.get("height"))

    def test_home_avatar_is_small_and_high_priority(self):
        home = next(p for p in pages() if p.url == "/")
        avatar = home.find("img")[0]
        self.assertEqual(avatar.get("fetchpriority"), "high")
        self.assertNotEqual(avatar.get("loading"), "lazy")
        candidates = [c.split()[0] for c in avatar["srcset"].split(",")] + [avatar["src"]]
        for src in candidates:
            with self.subTest(src=src):
                self.assertLess(os.path.getsize(public_file(src)), 40_000)

    def test_article_images_are_matted_and_only_larger_originals_link(self):
        # The mat is the wrapper, not padding on the img. A link exists only
        # when the render hook already decided the original is wider than
        # the 1500px cap; that link is the expand-mark target.
        for page in articles():
            for img, ancestors in images_in(page):
                with self.subTest(page=page.url, img=img.get("src")):
                    kind = mat_kind(ancestors)
                    self.assertIn(kind, ("full", "mat"))
                    linked = [a for tag, a in ancestors if tag == "a"]
                    if kind == "full":
                        self.assertEqual(len(linked), 1)
                        self.assertNotEqual(linked[0].get("href"), img.get("src"))
                        self.assertIn("view full size", linked[0].get("aria-label", ""))
                    else:
                        self.assertEqual(linked, [])

    def test_wide_originals_link_and_small_ones_do_not(self):
        # saying-goodbye photos are wider than 1500px. The grim reaper
        # sketch is 1024px and the luffy sketch is 500px, so neither has a
        # larger original. The GraphQL gif is not resized at all.
        by_url = {p.url: p for p in articles()}

        goodbye = images_in(by_url["/2015/saying-goodbye/"])
        self.assertTrue(any(mat_kind(a) == "full" for _, a in goodbye))

        grim = images_in(by_url["/2024/im-writing-again/"])
        self.assertEqual(len(grim), 1)
        self.assertIn("grim-reaper-writing-sketch", grim[0][0]["src"])
        self.assertEqual(mat_kind(grim[0][1]), "mat")

        luffy = images_in(by_url["/2013/5-am/"])
        self.assertEqual(len(luffy), 1)
        self.assertIn("luffy-sketch", luffy[0][0]["src"])
        self.assertEqual(mat_kind(luffy[0][1]), "mat")

        graphql = images_in(by_url["/2021/how-i-converted-a-rest-api-to-graphql/"])
        gif = next(img for img, _ in graphql if "rest-to-graphql" in img["src"])
        gif_ancestors = next(a for img, a in graphql if img is gif)
        self.assertEqual(mat_kind(gif_ancestors), "mat")
        self.assertTrue(any(mat_kind(a) == "full" for _, a in graphql))

    def test_the_mat_does_not_wrap_the_avatar(self):
        # The avatar, favicons, and other chrome are not article images.
        for page in pages():
            if page in articles():
                continue
            for img, ancestors in images_in(page):
                with self.subTest(page=page.url, img=img.get("src")):
                    self.assertIsNone(mat_kind(ancestors))

    def test_stylesheet_carries_the_mat_and_expand_mark(self):
        # The mark is a CSS pseudo-element. Minify may rewrite numbers, but
        # the mat, the zoom cursor, and the two arrow strokes have to survive.
        hrefs = {a["href"] for p in pages() for a in p.find("link", rel="stylesheet")}
        css = ""
        for href in hrefs:
            with open(public_file(href), encoding="utf-8") as f:
                css += f.read()
        self.assertIn("img-mat", css)
        self.assertIn("zoom-in", css)
        self.assertIn("fit-content", css)
        self.assertIn("#d0d0d0", css)
        self.assertIn("focus-visible", css)
        self.assertTrue(
            "M9.5 2.5" in css or "M9.5%202.5" in css,
            "expand-mark svg missing from the stylesheet",
        )
        self.assertNotIn("img-full:focus-visible{outline:none", css.replace(" ", ""))
        self.assertNotIn("img-full:focus-visible{outline:0", css.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
