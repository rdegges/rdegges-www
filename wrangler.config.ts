import { defineWranglerConfig } from "wrangler/experimental-config";

// Only the assets directory lives here; cloudflare.config.ts owns everything else.
export default defineWranglerConfig({
  "assetsDirectory": "public"
});
