"""Every post shows when it was published, in a machine-readable <time>."""

import unittest
from datetime import date

from helpers import SiteTestCase, articles


class TestPostDates(SiteTestCase):
    def test_every_post_has_a_dated_time_element(self):
        for page in articles():
            with self.subTest(page=page.url):
                times = [a for t, a in page.tags if t == "time" and "datetime" in a]
                self.assertEqual(len(times), 1)
                published = date.fromisoformat(times[0]["datetime"])
                # The URL's year and the shown date must agree.
                self.assertEqual(str(published.year), page.url[1:5])

    def test_date_is_shown_under_the_title(self):
        for page in articles():
            with self.subTest(page=page.url):
                order = [t for t, _ in page.tags if t in ("h1", "time")]
                i = order.index("time")
                self.assertEqual(order[i - 1], "h1", "the date should follow the post's <h1>")


if __name__ == "__main__":
    unittest.main()
