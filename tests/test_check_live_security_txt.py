"""scripts/check-live-security-txt.sh, which the deploy job runs after every
deploy to main.

The script is run for real, with bash and GNU date, but curl and sleep are
stubs on PATH: each test says what the "live site" serves on each attempt,
and no test touches the network or waits 15 seconds between attempts.

Unlike the other test files, this one needs no built site.
"""

import os
import re
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "scripts", "check-live-security-txt.sh")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "build.yml")
URL = "https://rdegges.com/.well-known/security.txt"


def gnu_date():
    """The script parses Expires with GNU date -d, as on the CI runner."""
    try:
        return subprocess.run(["date", "-u", "-d", "@0", "+%s"], capture_output=True, text=True).stdout.strip() == "0"
    except OSError:
        return False


def stamp(delta):
    return (datetime.now(timezone.utc) + delta).strftime("%Y-%m-%dT%H:%M:%SZ")


def security_txt(*expires):
    lines = ["Contact: mailto:r@rdegges.com"]
    lines += [f"Expires: {e}" for e in expires]
    lines += ["Preferred-Languages: en", f"Canonical: {URL}"]
    return "\n".join(lines) + "\n"


# Attempt n serves $STUB/n.body, or fails like curl --fail does when there is
# no such file. Every call appends its arguments to $STUB/curl.log.
CURL = textwrap.dedent(
    """\
    #!/usr/bin/env bash
    n=$(( $(wc -l < "$STUB/curl.log") + 1 ))
    printf '%s\\n' "$*" >> "$STUB/curl.log"
    if [ -f "$STUB/$n.body" ]; then cat "$STUB/$n.body"; exit 0; fi
    echo "curl: (22) The requested URL returned error: 503" >&2
    exit 22
    """
)
SLEEP = '#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$STUB/sleep.log"\n'


@unittest.skipUnless(gnu_date() and shutil.which("bash"), "needs bash and GNU date, like the CI runner")
class TestCheckLiveSecurityTxt(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)
        self.stub = os.path.join(self.dir, "stub")
        bin_dir = os.path.join(self.dir, "bin")
        os.mkdir(self.stub)
        os.mkdir(bin_dir)
        for name, body in (("curl", CURL), ("sleep", SLEEP)):
            path = os.path.join(bin_dir, name)
            with open(path, "w") as f:
                f.write(body)
            os.chmod(path, 0o755)
        for log in ("curl.log", "sleep.log"):
            open(os.path.join(self.stub, log), "w").close()
        self.env = dict(os.environ, STUB=self.stub, PATH=bin_dir + os.pathsep + os.environ["PATH"])
        self.packaged = os.path.join(self.dir, "security.txt")
        # A build a few minutes ago; whole days stay clear of a boundary.
        self.want = stamp(timedelta(days=180) - timedelta(minutes=5))

    def package(self, text):
        with open(self.packaged, "w") as f:
            f.write(text)

    def serve(self, *bodies):
        """Body per attempt; None means that attempt's fetch fails."""
        for n, body in enumerate(bodies, start=1):
            if body is not None:
                with open(os.path.join(self.stub, f"{n}.body"), "w") as f:
                    f.write(body)

    def run_script(self, *args):
        if not args:
            args = (self.packaged, URL)
        return subprocess.run([SCRIPT, *args], env=self.env, capture_output=True, text=True, timeout=30)

    def log(self, name):
        with open(os.path.join(self.stub, name)) as f:
            return f.read().splitlines()

    def assertFailsBeforeFetching(self, result, message):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)
        self.assertIn("::error::", result.stdout)
        self.assertEqual(self.log("curl.log"), [], "must not fetch when the package itself is wrong")

    # Live site matches the package.

    def test_passes_on_first_attempt_when_live_matches(self):
        self.package(security_txt(self.want))
        self.serve(security_txt(self.want))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stdout, rf"^ok: {re.escape(URL)} serves Expires {self.want}, 179 days out$")
        self.assertEqual(len(self.log("curl.log")), 1)
        self.assertEqual(self.log("sleep.log"), [])

    def test_fetches_only_over_https_and_fails_on_http_errors(self):
        self.package(security_txt(self.want))
        self.serve(security_txt(self.want))
        self.run_script()
        args = self.log("curl.log")[0].split()
        self.assertIn("--fail", args)
        self.assertEqual(args[args.index("--proto") + 1], "=https")
        self.assertIn("--max-time", args)
        self.assertEqual(args[-1], URL)

    def test_waits_for_the_new_version_to_propagate(self):
        stale = security_txt(stamp(timedelta(days=150)))
        self.package(security_txt(self.want))
        self.serve(stale, None, security_txt(self.want))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("attempt 1: ", result.stdout)
        self.assertIn("attempt 2: could not fetch", result.stdout)
        self.assertEqual(len(self.log("curl.log")), 3)
        self.assertEqual(self.log("sleep.log"), ["15", "15"])

    # Live site never matches: fails closed after six attempts.

    def test_fails_when_live_keeps_serving_an_older_deploy(self):
        # The case a "more than N days out" threshold would miss: the old
        # file is still valid, but it is not this deploy.
        old = security_txt(stamp(timedelta(days=179, hours=23)))
        self.package(security_txt(self.want))
        self.serve(*[old] * 6)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("::error::", result.stdout)
        self.assertEqual(len(self.log("curl.log")), 6)
        self.assertEqual(self.log("sleep.log"), ["15"] * 5, "no sleep after the last attempt")

    def test_fails_when_live_cannot_be_fetched(self):
        self.package(security_txt(self.want))
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count("could not fetch"), 6)
        self.assertIn("::error::", result.stdout)

    def test_fails_when_live_has_two_expires_lines(self):
        # Even if both equal the packaged value: readers would have to pick.
        self.package(security_txt(self.want))
        self.serve(*[security_txt(self.want, self.want)] * 6)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("not exactly one Expires line", result.stdout)

    def test_fails_when_live_has_no_expires_line(self):
        self.package(security_txt(self.want))
        self.serve(*[security_txt()] * 6)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("not exactly one Expires line", result.stdout)

    def test_fails_when_live_serves_an_html_error_page(self):
        self.package(security_txt(self.want))
        self.serve(*["<!doctype html><title>Not found</title>\n"] * 6)
        self.assertEqual(self.run_script().returncode, 1)

    # The package is wrong: fails before fetching anything.

    def test_packaged_file_missing(self):
        result = self.run_script(os.path.join(self.dir, "missing.txt"), URL)
        self.assertFailsBeforeFetching(result, "exactly one Expires line")

    def test_packaged_file_without_expires(self):
        self.package(security_txt())
        self.assertFailsBeforeFetching(self.run_script(), "exactly one Expires line")

    def test_packaged_file_with_two_expires_lines(self):
        self.package(security_txt(self.want, self.want))
        self.assertFailsBeforeFetching(self.run_script(), "exactly one Expires line")

    def test_packaged_expires_not_a_date(self):
        self.package(security_txt("next spring"))
        self.assertFailsBeforeFetching(self.run_script(), "cannot read the packaged Expires value 'next spring'")

    def test_packaged_expires_too_soon(self):
        # A template change to a shorter window must not pass as "renewed".
        self.package(security_txt(stamp(timedelta(days=90, hours=1))))
        self.assertFailsBeforeFetching(self.run_script(), "expires in 90 days")

    def test_packaged_expires_threshold_is_179_whole_days(self):
        self.package(security_txt(stamp(timedelta(days=178, hours=23))))
        self.assertFailsBeforeFetching(self.run_script(), "expires in 178 days")

        just_enough = stamp(timedelta(days=179, minutes=5))
        self.package(security_txt(just_enough))
        self.serve(security_txt(just_enough))
        self.assertEqual(self.run_script().returncode, 0)

    def test_packaged_expires_in_the_past(self):
        self.package(security_txt(stamp(-timedelta(days=1))))
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.log("curl.log"), [])

    # Usage.

    def test_wrong_argument_count_is_a_usage_error(self):
        for args in ((self.packaged,), (self.packaged, URL, "extra")):
            result = self.run_script(*args)
            self.assertEqual(result.returncode, 2, args)
            self.assertIn("usage:", result.stderr)
        self.assertEqual(self.log("curl.log"), [])


class TestDeployRunsTheCheck(unittest.TestCase):
    """The wiring in build.yml. Text checks: the standard library has no YAML."""

    def setUp(self):
        with open(WORKFLOW, encoding="utf-8") as f:
            self.workflow = f.read()

    def test_script_is_executable(self):
        # The workflow runs it as ./scripts/..., so a lost mode bit fails the deploy.
        self.assertTrue(os.stat(SCRIPT).st_mode & stat.S_IXUSR)

    def test_runs_on_a_monthly_schedule(self):
        cron = re.search(r'^\s*schedule:\s*\n\s*- cron: "([^"]+)"', self.workflow, re.M)
        self.assertIsNotNone(cron)
        minute, hour, day, month, weekday = cron[1].split()
        # Monthly leaves room for a lost run or two inside the 180 days.
        self.assertEqual((day, month, weekday), ("1", "*", "*"))

    def test_deploy_job_admits_scheduled_runs(self):
        deploy = self.workflow.split("\n  deploy:\n", 1)[1].split("\n  zizmor:\n", 1)[0]
        self.assertIn("if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'", deploy)

    def test_deploy_checks_the_uploaded_file_against_the_canonical_url(self):
        deploy = self.workflow.split("\n  deploy:\n", 1)[1].split("\n  zizmor:\n", 1)[0]
        steps = deploy.split("- name: ")
        names = [s.splitlines()[0] for s in steps[1:]]
        # After the deploy step, so it checks what was just uploaded.
        self.assertEqual(names[-2:], ["Deploy to Cloudflare", "Check the live security.txt"])
        run = re.search(r"run: (\S+) (\S+) (\S+)\s*$", steps[-1].strip(), re.M)
        self.assertIsNotNone(run)
        script, packaged, url = run.groups()
        self.assertEqual(script, "./scripts/check-live-security-txt.sh")
        # The same assets directory the pre-deploy step checks and cf uploads.
        self.assertIn("assets=.cloudflare/output/v0/workers/default/assets", deploy)
        self.assertEqual(packaged, ".cloudflare/output/v0/workers/default/assets/.well-known/security.txt")
        # The Canonical value test_security_txt.py pins for the built file.
        self.assertEqual(url, URL)
        self.assertNotIn("${{", steps[-1], "no expressions or secrets in the check step")


if __name__ == "__main__":
    unittest.main()
