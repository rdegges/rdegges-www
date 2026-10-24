import { defineConfig } from "cf/config";

// Runtime settings live here; wrangler.config.ts owns only the assets directory.
export default defineConfig({
  worker: {
    "name": "rdegges-www",
    "compatibilityDate": "2026-10-19",
    "assets": {
      "notFoundHandling": "404-page"
    }
  }
});
