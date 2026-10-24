"""/.well-known/security.txt follows RFC 9116."""

import os
import re
import unittest
from datetime import datetime, timedelta, timezone

from helpers import PUBLIC, SiteTestCase, pages, public_file

PATH = os.path.join(PUBLIC, ".well-known", "security.txt")

# RFC 9116 section 4: field lines are "Name: value", comments start with "#".
FIELD = re.compile(r"^([A-Za-z0-9-]+): (\S.*)$")


class TestSecurityTxt(SiteTestCase):
    def setUp(self):
        with open(PATH, "rb") as f:
            self.raw = f.read()
        self.lines = self.raw.decode("utf-8").splitlines()
        self.fields = {}
        for line in self.lines:
            match = FIELD.match(line)
            if match:
                self.fields.setdefault(match[1], []).append(match[2])

    def test_every_line_is_a_field_or_comment(self):
        # A stray template line (an unclosed comment, a blank from a trim
        # marker) would be silently ignored by a lenient parser.
        bad = [l for l in self.lines if not (FIELD.match(l) or l.startswith("#"))]
        self.assertEqual(bad, [])

    def test_every_line_ends_with_a_newline(self):
        # The RFC's grammar ends every line, the last one too, with an eol.
        self.assertTrue(self.raw.endswith(b"\n"))

    def test_required_fields(self):
        self.assertEqual(self.fields["Contact"], ["mailto:r@rdegges.com"])
        self.assertEqual(len(self.fields["Expires"]), 1)

    def test_optional_fields_appear_at_most_once(self):
        for name in ("Canonical", "Preferred-Languages"):
            self.assertLessEqual(len(self.fields.get(name, [])), 1, name)
        self.assertEqual(self.fields["Preferred-Languages"], ["en"])

    def test_expires_is_an_internet_date_time(self):
        # RFC 3339 date-time, which fromisoformat alone does not enforce: it
        # also accepts a bare date or a space instead of the "T".
        self.assertRegex(self.fields["Expires"][0], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(Z|[+-]\d\d:\d\d)$")

    def test_expires_is_in_the_future_but_under_a_year(self):
        expires = datetime.fromisoformat(self.fields["Expires"][0].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        self.assertGreater(expires, now + timedelta(days=30))
        self.assertLess(expires, now + timedelta(days=365))

    def test_canonical_url_is_where_the_file_is(self):
        self.assertEqual(self.fields["Canonical"], ["https://rdegges.com/.well-known/security.txt"])
        self.assertTrue(os.path.isfile(public_file("/.well-known/security.txt")))

    def test_not_advertised_from_any_page(self):
        # notAlternative in hugo.toml keeps it out of every page's <head>.
        linked = [p.url for p in pages(include_aliases=True) if any("security.txt" in (a.get("href") or "") for a in p.find("link"))]
        self.assertEqual(linked, [])

    def test_not_in_the_sitemap(self):
        with open(public_file("/sitemap.xml"), encoding="utf-8") as f:
            self.assertNotIn("security.txt", f.read())


if __name__ == "__main__":
    unittest.main()
