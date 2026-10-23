"""/.well-known/security.txt follows RFC 9116."""

import os
import unittest
from datetime import datetime, timedelta, timezone

from helpers import PUBLIC, SiteTestCase


class TestSecurityTxt(SiteTestCase):
    def setUp(self):
        with open(os.path.join(PUBLIC, ".well-known", "security.txt"), encoding="utf-8") as f:
            self.fields = {}
            for line in f:
                name, _, value = line.partition(":")
                self.fields.setdefault(name.strip(), []).append(value.strip())

    def test_required_fields(self):
        self.assertTrue(self.fields["Contact"][0].startswith("mailto:"))
        self.assertEqual(len(self.fields["Expires"]), 1)

    def test_expires_is_in_the_future_but_under_a_year(self):
        expires = datetime.fromisoformat(self.fields["Expires"][0].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        self.assertGreater(expires, now + timedelta(days=30))
        self.assertLess(expires, now + timedelta(days=365))

    def test_canonical_url(self):
        self.assertEqual(self.fields["Canonical"], ["https://rdegges.com/.well-known/security.txt"])


if __name__ == "__main__":
    unittest.main()
