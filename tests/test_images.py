"""Images reserve their space and stay small."""

import os
import unittest

from helpers import SiteTestCase, pages, public_file


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


if __name__ == "__main__":
    unittest.main()
