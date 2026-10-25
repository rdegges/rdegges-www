import { defineConfig } from "cf/config";

// Runtime settings live here; wrangler.config.ts owns only the assets directory.
export default defineConfig({
  worker: {
    "name": "rdegges-www",
    "compatibilityDate": "2026-10-19",
    // rdegges.com serves the site. A second public copy would split search
    // results, and cf deploy turns workers.dev on unless this says no.
    // Preview URLs are off for the same reason; CI never uses them.
    "workersDev": false,
    "previewUrls": false,
    "assets": {
      "notFoundHandling": "404-page"
    }
  }
});
