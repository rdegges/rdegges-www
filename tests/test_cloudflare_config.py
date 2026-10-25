"""cloudflare.config.ts keeps the workers.dev copy of the site turned off."""

import os
import re
import unittest

CONFIG = os.path.join(os.path.dirname(__file__), "..", "cloudflare.config.ts")


def config_code():
    """cloudflare.config.ts with // comments removed, so prose cannot match."""
    with open(CONFIG, encoding="utf-8") as f:
        return re.sub(r"//.*", "", f.read())


class TestCloudflareConfig(unittest.TestCase):
    def test_workers_dev_is_off(self):
        # With no routes in the config, cf deploy turns the workers.dev URL on
        # unless workersDev says otherwise. That URL serves the whole site
        # without noindex: a second copy for search engines to find.
        settings = re.findall(r"""["']?workersDev["']?\s*:\s*(\w+)""", config_code())
        self.assertEqual(settings, ["false"])

    def test_preview_urls_are_off(self):
        # cf leaves preview URLs as they are unless previewUrls says otherwise,
        # and each one serves a whole version of the site on workers.dev.
        settings = re.findall(r"""["']?previewUrls["']?\s*:\s*(\w+)""", config_code())
        self.assertEqual(settings, ["false"])

    def test_config_lists_no_routes(self):
        # The custom domain was attached by hand, and the deploy token cannot
        # change routes or custom domains. A route here would make every
        # deploy fail on permissions.
        self.assertNotRegex(config_code(), r"""["']?(routes|route|customDomain)["']?\s*:""")


if __name__ == "__main__":
    unittest.main()
