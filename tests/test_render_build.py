"""scripts/render-build.sh, the production build that Render and CI both run.

The script is run for real, with bash and GNU coreutils, in a scratch copy of
the repository layout. curl is a stub on PATH that serves local fixtures, so
no test touches the network: each test says what the "release page" serves for
the Hugo archive and for its checksums file. The archive holds a stub `hugo`
that only records how it was called, so a test can tell whether the script ran
the binary it had just downloaded.

Every rejection case must exit non-zero, never run hugo, and leave nothing
behind in TMPDIR (no partly installed binary). The Hugo version is read from
docker-compose.yml, as the script does, so a Dependabot bump of that tag
needs no change here.

Unlike the other test files, this one needs no built site.
"""

import gzip
import hashlib
import io
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import textwrap
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "scripts", "render-build.sh")
COMPOSE = os.path.join(ROOT, "docker-compose.yml")

with open(COMPOSE, encoding="utf-8") as f:
    VERSION = re.search(r"^\s*image:\s*ghcr\.io/gohugoio/hugo:v([0-9.]+)\s*$", f.read(), re.M)[1]

ARCHIVE = f"hugo_{VERSION}_linux-amd64.tar.gz"
BASE = f"https://github.com/gohugoio/hugo/releases/download/v{VERSION}"
ARCHIVE_URL = f"{BASE}/{ARCHIVE}"
CHECKSUMS_URL = f"{BASE}/hugo_{VERSION}_checksums.txt"

# Serves $STUB/serve/<last URL segment>. A missing file is a 404: curl --fail
# exits 22, and without it curl would "succeed" with an error page, which is
# what the stub does too. A <name>.exit file makes the fetch exit with that
# status after writing the (partial) body, like an interrupted transfer.
CURL = textwrap.dedent(
    """\
    #!/usr/bin/env bash
    out=""; fail=0; url=""
    while [ $# -gt 0 ]; do
      case "$1" in
        -o) out=$2; shift 2; continue ;;
        --fail) fail=1 ;;
        -[!-]*) case "$1" in *f*) fail=1 ;; esac ;;
        -*) ;;
        *) url=$1 ;;
      esac
      shift
    done
    printf '%s\\n' "$url" >> "$STUB/curl.log"
    name=${url##*/}
    if [ -f "$STUB/serve/$name" ]; then
      cat "$STUB/serve/$name" > "${out:-/dev/stdout}"
      if [ -f "$STUB/serve/$name.exit" ]; then exit "$(cat "$STUB/serve/$name.exit")"; fi
      exit 0
    fi
    if [ "$fail" = 1 ]; then
      echo "curl: (22) The requested URL returned error: 404" >&2
      exit 22
    fi
    echo "Not Found" > "${out:-/dev/stdout}"
    """
)

# Used for the hugo inside the archive and for a hugo that is already on PATH:
# either one running is recorded.
HUGO = textwrap.dedent(
    """\
    #!/usr/bin/env bash
    printf '%s\\n' "$*" >> "$STUB/hugo.log"
    exit "${FAKE_HUGO_EXIT:-0}"
    """
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def tarball(members=("hugo", "LICENSE", "README.md")):
    """A .tar.gz shaped like Hugo's release archive, with a stub hugo."""
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        for name in members:
            data = HUGO.encode() if name == "hugo" else f"{name}\n".encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o755 if name == "hugo" else 0o644
            tar.addfile(info, io.BytesIO(data))
    return gzip.compress(raw.getvalue(), mtime=0)


def sibling_lines():
    """Lines for the other artifacts of the release, as in Hugo's real file."""
    names = [
        f"hugo_extended_{VERSION}_linux-amd64.tar.gz",
        f"hugo_extended_withdeploy_{VERSION}_linux-amd64.tar.gz",
        f"hugo_withdeploy_{VERSION}_linux-amd64.tar.gz",
        f"hugo_{VERSION}_linux-amd64.deb",
        f"hugo_{VERSION}_darwin-universal.tar.gz",
    ]
    return [f"{sha256(n.encode())}  {n}" for n in names]


def checksums(*lines):
    return ("\n".join(lines) + "\n").encode() if lines else b""


def bash_available():
    return all(shutil.which(t) for t in ("bash", "sha256sum", "tar", "mktemp"))


@unittest.skipUnless(bash_available(), "needs bash and GNU coreutils, like the CI runner")
class TestRenderBuild(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)
        self.root = os.path.join(self.dir, "repo")
        self.stub = os.path.join(self.dir, "stub")
        self.tmp = os.path.join(self.dir, "tmp")
        bin_dir = os.path.join(self.dir, "bin")
        os.makedirs(os.path.join(self.root, "scripts"))
        os.makedirs(os.path.join(self.stub, "serve"))
        os.mkdir(self.tmp)
        os.mkdir(bin_dir)
        shutil.copy2(SCRIPT, os.path.join(self.root, "scripts", "render-build.sh"))
        shutil.copy2(COMPOSE, os.path.join(self.root, "docker-compose.yml"))
        for name, body in (("curl", CURL), ("hugo", HUGO)):
            path = os.path.join(bin_dir, name)
            with open(path, "w") as f:
                f.write(body)
            os.chmod(path, 0o755)
        for log in ("curl.log", "hugo.log"):
            open(os.path.join(self.stub, log), "w").close()
        # What Render sets does not matter to the script; HUGO_VERSION is
        # ignored by Render's own image, and must be ignored here too.
        self.env = dict(
            os.environ,
            STUB=self.stub,
            TMPDIR=self.tmp,
            PATH=bin_dir + os.pathsep + os.environ["PATH"],
            RENDER="true",
            HUGO_VERSION="0.124.0",
        )
        self.archive = tarball()
        self.serve_release()

    def serve(self, name, data, exit_status=None):
        with open(os.path.join(self.stub, "serve", name), "wb") as f:
            f.write(data)
        if exit_status is not None:
            with open(os.path.join(self.stub, "serve", name + ".exit"), "w") as f:
                f.write(str(exit_status))

    def unserve(self, name):
        os.remove(os.path.join(self.stub, "serve", name))

    def serve_release(self, archive=None, sums=None):
        archive = self.archive if archive is None else archive
        if sums is None:
            sums = checksums(*sibling_lines(), f"{sha256(archive)}  {ARCHIVE}")
        self.serve(ARCHIVE, archive)
        self.serve(f"hugo_{VERSION}_checksums.txt", sums)

    def run_script(self, *args):
        return subprocess.run(
            [os.path.join(self.root, "scripts", "render-build.sh"), *args],
            env=self.env,
            cwd=self.dir,
            capture_output=True,
            text=True,
            timeout=60,
        )

    def log(self, name):
        with open(os.path.join(self.stub, name)) as f:
            return f.read().splitlines()

    def assertRejected(self, result, message=None):
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        if message:
            self.assertIn(message, output)
        self.assertEqual(self.log("hugo.log"), [], "hugo must not run after a failed download or check")
        self.assertEqual(os.listdir(self.tmp), [], "the script must remove everything it put in TMPDIR")

    # The good path.

    def test_installs_and_runs_the_verified_plain_archive(self):
        result = self.run_script("--panicOnWarning")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"{ARCHIVE}: OK", result.stdout)
        # Exactly these two fetches, and neither is the extended edition.
        self.assertEqual(self.log("curl.log"), [ARCHIVE_URL, CHECKSUMS_URL])
        self.assertNotIn("extended", " ".join(self.log("curl.log")))
        # The hugo from the archive ran, with the build flag and CI's extras.
        self.assertEqual(self.log("hugo.log"), ["version", "--minify --panicOnWarning"])
        self.assertEqual(os.listdir(self.tmp), [])

    def test_uses_the_version_in_docker_compose_not_the_environment(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"Downloading Hugo {VERSION}", result.stdout)
        self.assertNotIn("0.124.0", " ".join(self.log("curl.log")))

    def test_hugo_failure_fails_the_build_and_cleans_up(self):
        self.env["FAKE_HUGO_EXIT"] = "3"
        result = self.run_script()
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertEqual(os.listdir(self.tmp), [])

    def test_unreadable_version_fails_before_downloading(self):
        with open(os.path.join(self.root, "docker-compose.yml"), "w") as f:
            f.write("services:\n  hugo:\n    build: .\n")
        result = self.run_script()
        self.assertRejected(result, "could not read the Hugo version")
        self.assertEqual(self.log("curl.log"), [])

    # The archive is not what Hugo published.

    def test_rejects_a_corrupted_archive(self):
        good = self.archive
        flipped = bytearray(good)
        flipped[len(flipped) // 2] ^= 0x01
        # Checksums still describe the genuine archive.
        self.serve_release(archive=bytes(flipped), sums=checksums(*sibling_lines(), f"{sha256(good)}  {ARCHIVE}"))
        self.assertRejected(self.run_script(), "FAILED")

    def test_rejects_a_wrong_hash_in_the_checksums_file(self):
        wrong = sha256(b"not the archive")
        self.serve_release(sums=checksums(*sibling_lines(), f"{wrong}  {ARCHIVE}"))
        self.assertRejected(self.run_script(), "FAILED")

    def test_rejects_a_truncated_archive_that_curl_reports_as_complete(self):
        self.serve_release(sums=checksums(*sibling_lines(), f"{sha256(self.archive)}  {ARCHIVE}"))
        self.serve(ARCHIVE, self.archive[: len(self.archive) // 2])
        self.assertRejected(self.run_script(), "FAILED")

    def test_rejects_a_truncated_download_that_curl_reports_as_failed(self):
        # curl exit 18: partial file transferred.
        self.serve(ARCHIVE, self.archive[: len(self.archive) // 2], exit_status=18)
        self.assertRejected(self.run_script())
        self.assertEqual(self.log("curl.log"), [ARCHIVE_URL], "no point fetching checksums after a failed download")

    def test_rejects_an_archive_without_a_hugo_binary(self):
        # Right hash, wrong contents: tar finds nothing to install.
        self.serve_release(archive=tarball(members=("LICENSE", "README.md")))
        self.assertRejected(self.run_script())

    # The checksums file does not have exactly one line for the archive.

    def test_rejects_a_checksums_file_without_the_archive_line(self):
        self.serve_release(sums=checksums(*sibling_lines()))
        self.assertRejected(self.run_script(), "expected exactly one checksum")

    def test_rejects_an_empty_checksums_file(self):
        self.serve_release(sums=b"")
        self.assertRejected(self.run_script(), "expected exactly one checksum")

    def test_rejects_a_truncated_checksums_file(self):
        line = f"{sha256(self.archive)}  {ARCHIVE}"
        self.serve_release(sums=checksums(*sibling_lines()) + line[: len(line) // 2].encode())
        self.assertRejected(self.run_script())

    def test_rejects_a_duplicate_archive_line(self):
        line = f"{sha256(self.archive)}  {ARCHIVE}"
        self.serve_release(sums=checksums(*sibling_lines(), line, line))
        self.assertRejected(self.run_script(), "expected exactly one checksum")

    def test_rejects_conflicting_lines_for_the_archive(self):
        # One right, one wrong: must not pass because one of them matches.
        right = f"{sha256(self.archive)}  {ARCHIVE}"
        wrong = f"{sha256(b'other')}  {ARCHIVE}"
        for order in ((right, wrong), (wrong, right)):
            with self.subTest(order="right first" if order[0] == right else "wrong first"):
                self.serve_release(sums=checksums(*sibling_lines(), *order))
                self.assertRejected(self.run_script(), "expected exactly one checksum")

    def test_rejects_lines_only_for_similarly_named_archives(self):
        # Hugo publishes hugo_extended_*, hugo_withdeploy_* and
        # hugo_extended_withdeploy_* beside the plain archive. A substring
        # match would take one of them for the archive; even with a correct
        # hash for our file, only the exact name counts.
        digest = sha256(self.archive)
        impostors = (
            f"hugo_extended_{VERSION}_linux-amd64.tar.gz",
            f"hugo_withdeploy_{VERSION}_linux-amd64.tar.gz",
            f"hugo_extended_withdeploy_{VERSION}_linux-amd64.tar.gz",
            f"{ARCHIVE}.sig",
            f"x{ARCHIVE}",
            f"prefix/{ARCHIVE}",
        )
        for name in impostors:
            with self.subTest(name=name):
                self.serve_release(sums=checksums(f"{digest}  {name}"))
                self.assertRejected(self.run_script(), "expected exactly one checksum")

    def test_a_full_realistic_checksums_file_passes(self):
        # The sibling lines alone must not break the exact-match check.
        digest = sha256(self.archive)
        lines = sibling_lines()
        self.serve_release(sums=checksums(lines[0], lines[1], f"{digest}  {ARCHIVE}", *lines[2:]))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    # A download fails outright.

    def test_rejects_a_404_for_the_archive(self):
        self.unserve(ARCHIVE)
        result = self.run_script()
        self.assertRejected(result, "404")
        self.assertEqual(self.log("curl.log"), [ARCHIVE_URL])

    def test_rejects_a_404_for_the_checksums_file(self):
        self.unserve(f"hugo_{VERSION}_checksums.txt")
        result = self.run_script()
        self.assertRejected(result, "404")
        self.assertEqual(self.log("curl.log"), [ARCHIVE_URL, CHECKSUMS_URL])

    def test_rejects_an_error_page_served_with_a_success_status(self):
        # Defense in depth beside curl --fail: an HTML error page in place of
        # the checksums file has no archive line.
        self.serve(f"hugo_{VERSION}_checksums.txt", b"<html>Not Found</html>\n")
        self.assertRejected(self.run_script(), "expected exactly one checksum")


if __name__ == "__main__":
    unittest.main()
