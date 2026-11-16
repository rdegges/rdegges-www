"""The Hugo pin: one version, in docker-compose.yml, and nothing that disagrees.

docker-compose.yml's image tag is the single source of truth for the Hugo
version. scripts/render-build.sh reads it (CI and Render both run that script),
and the README documents it. These tests do not hard-code a version, so a
Dependabot bump of the tag needs no change here; they fail when the pin is
malformed, when a second copy of the version appears that can drift, or when
the documentation or the older-Hugo floor in hugo.toml disagrees with the tag.

Unlike the other test files, these need no built site and make no network
requests, except for TestPublishedRelease, which is skipped unless
HUGO_PIN_ONLINE=1 is set. That class asks GitHub and ghcr.io whether the pinned
tag, its archive checksum and its docker image really exist.
"""

import hashlib
import os
import re
import unittest
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

IMAGE_RE = re.compile(r"^\s*image:\s*(\S+)\s*$", re.M)
TAG_RE = re.compile(r"^ghcr\.io/gohugoio/hugo:v(\d+)\.(\d+)\.(\d+)$")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def pinned_version():
    images = IMAGE_RE.findall(read("docker-compose.yml"))
    assert len(images) == 1, images
    m = TAG_RE.match(images[0])
    assert m, images[0]
    return ".".join(m.groups())


def as_tuple(version):
    return tuple(int(p) for p in version.split("."))


def tracked_text_files():
    """Config and script files that could carry a second copy of the version."""
    skip_dirs = {".git", "content", "public", "resources", "node_modules", ".cloudflare", "tests", "static"}
    skip_files = {"package-lock.json"}
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for name in files:
            if name in skip_files:
                continue
            path = os.path.join(base, name)
            try:
                with open(path, encoding="utf-8") as f:
                    yield os.path.relpath(path, ROOT), f.read()
            except (UnicodeDecodeError, OSError):
                continue


class TestComposePin(unittest.TestCase):
    def test_exactly_one_image_and_it_is_the_official_hugo_image(self):
        images = IMAGE_RE.findall(read("docker-compose.yml"))
        self.assertEqual(len(images), 1, images)
        self.assertRegex(images[0], TAG_RE, "the tag must be exactly ghcr.io/gohugoio/hugo:vX.Y.Z")

    def test_tag_is_not_floating_and_has_no_digest_override(self):
        compose = read("docker-compose.yml")
        for bad in ("latest", "@sha256", "-ext", "-extended", "-withdeploy"):
            self.assertNotIn(bad, re.search(r"^\s*image:.*$", compose, re.M)[0])

    def test_pinned_version_is_not_older_than_the_template_floor(self):
        # hugo.toml's [module.hugoVersion] min is the oldest Hugo the layouts
        # support; the pin must never fall below it.
        floor = re.search(r"\[module\.hugoVersion\]\s*\n(?:#.*\n)*\s*min\s*=\s*\"(\d+\.\d+\.\d+)\"", read("hugo.toml"))
        self.assertIsNotNone(floor, "hugo.toml must declare [module.hugoVersion] min")
        self.assertGreaterEqual(as_tuple(pinned_version()), as_tuple(floor[1]))


class TestNoSecondCopy(unittest.TestCase):
    def test_nothing_else_names_the_hugo_image_or_release_url(self):
        allowed = {"docker-compose.yml", "README.md"}
        for path, text in tracked_text_files():
            if path in allowed:
                continue
            with self.subTest(path=path):
                self.assertNotIn("ghcr.io/gohugoio/hugo", text)
                # The script builds the URL from the version it read.
                for m in re.finditer(r"gohugoio/hugo/releases/download/v([^\s\"']*)", text):
                    self.assertTrue(m[1].startswith("${"), f"{path} hard-codes a release version: {m[0]}")

    def test_no_literal_hugo_version_in_scripts_or_workflows(self):
        literal = re.compile(r"hugo_(?:extended_)?(?:withdeploy_)?\d|\bv?0\.1\d\d\.\d+\b")
        for path, text in tracked_text_files():
            if not (path.startswith(".github/") or path.startswith("scripts/") or path in ("render.yaml", "Makefile")):
                continue
            # Comments may mention versions (the script explains 0.124.x and 0.170.0).
            code = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
            with self.subTest(path=path):
                self.assertIsNone(literal.search(code), f"{path} hard-codes a Hugo version")

    def test_no_environment_variable_or_action_sets_a_hugo_version(self):
        # Render ignores HUGO_VERSION, so setting it would only suggest a
        # second source of truth; actions-hugo would be an unchecked download.
        patterns = (
            r"^\s*-?\s*(?:key:\s*)?HUGO_VERSION\s*[:=]",
            r"hugo-version\s*:",
            r"peaceiris/actions-hugo",
            r"\bextended\s*[:=]\s*true",
        )
        for path, text in tracked_text_files():
            if not (path.startswith(".github/") or path in ("render.yaml", "Makefile", "hugo.toml")):
                continue
            for pattern in patterns:
                with self.subTest(path=path, pattern=pattern):
                    self.assertIsNone(re.search(pattern, text, re.M), f"{path} sets a Hugo version outside docker-compose.yml")
            self.assertNotRegex(text, r"key:\s*HUGO_VERSION")

    def test_no_other_toolchain_file_pins_hugo(self):
        for name in (".devcontainer", ".devcontainer.json", "Dockerfile", ".tool-versions", "netlify.toml", "vercel.json", ".mise.toml"):
            self.assertFalse(os.path.exists(os.path.join(ROOT, name)), f"{name} would be a second Hugo pin")

    def test_ci_and_render_both_build_through_the_script_that_reads_the_pin(self):
        self.assertRegex(read(".github", "workflows", "build.yml"), r"run:\s*\./scripts/render-build\.sh\b")
        self.assertRegex(read("render.yaml"), r"(?m)^\s*buildCommand:\s*\./scripts/render-build\.sh\s*$")
        # The workflow never calls a hugo binary of its own.
        for line in read(".github", "workflows", "build.yml").splitlines():
            if line.lstrip().startswith("run:"):
                self.assertNotRegex(line, r"(?<![\w/-])hugo\s")

    def test_script_downloads_the_plain_archive_for_the_version_it_read(self):
        script = read("scripts", "render-build.sh")
        self.assertIn('archive="hugo_${version}_linux-amd64.tar.gz"', script)
        self.assertIn('base="https://github.com/gohugoio/hugo/releases/download/v${version}"', script)
        self.assertIn('"${base}/hugo_${version}_checksums.txt"', script)
        code = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("#"))
        self.assertNotIn("hugo_extended", code)


class TestReadmeAgrees(unittest.TestCase):
    def test_every_version_the_readme_states_is_the_pinned_one(self):
        readme = read("README.md")
        version = pinned_version()
        stated = re.findall(r"ghcr\.io/gohugoio/hugo:v(\d+\.\d+\.\d+)", readme)
        stated += re.findall(r"[Tt]he pinned Hugo is v(\d+\.\d+\.\d+)", readme)
        self.assertTrue(stated, "the README must state the pinned version")
        self.assertEqual(set(stated), {version}, "the README disagrees with the tag in docker-compose.yml")

    def test_readme_does_not_describe_an_extended_download(self):
        readme = read("README.md")
        self.assertIn("plain `hugo_*`", readme)
        self.assertIn("SHA-256", readme)


@unittest.skipUnless(os.environ.get("HUGO_PIN_ONLINE") == "1", "set HUGO_PIN_ONLINE=1 to check GitHub and ghcr.io")
class TestPublishedRelease(unittest.TestCase):
    """The pinned tag exists, and its plain linux-amd64 archive matches its checksum."""

    @classmethod
    def setUpClass(cls):
        cls.version = pinned_version()
        cls.base = f"https://github.com/gohugoio/hugo/releases/download/v{cls.version}"
        cls.archive = f"hugo_{cls.version}_linux-amd64.tar.gz"

    def fetch(self, url, headers=None):
        request = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.read()

    def test_checksums_file_has_one_line_for_the_plain_archive_and_it_verifies(self):
        sums = self.fetch(f"{self.base}/hugo_{self.version}_checksums.txt").decode()
        lines = [line for line in sums.splitlines() if line.endswith(f"  {self.archive}")]
        self.assertEqual(len(lines), 1, lines)
        digest = lines[0].split()[0]
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        self.assertEqual(hashlib.sha256(self.fetch(f"{self.base}/{self.archive}")).hexdigest(), digest)

    def test_docker_image_tag_exists(self):
        token = self.fetch("https://ghcr.io/token?scope=repository:gohugoio/hugo:pull")
        token = re.search(rb'"token"\s*:\s*"([^"]+)"', token)[1].decode()
        request = urllib.request.Request(
            f"https://ghcr.io/v2/gohugoio/hugo/manifests/v{self.version}",
            method="HEAD",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json",
            },
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            self.assertEqual(response.status, 200)
            self.assertTrue(response.headers["docker-content-digest"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()
