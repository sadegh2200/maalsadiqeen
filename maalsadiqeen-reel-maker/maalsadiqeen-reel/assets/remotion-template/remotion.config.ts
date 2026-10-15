import path from "node:path";
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setConcurrency(1);

// Locked-down machines (CI, sandboxes) where Chrome cannot be downloaded: point
// REEL_CHROME_BRIDGE at an executable wrapper that starts your own headless-shell binary
// (see scripts/chrome-bridge.sh and references/troubleshooting.md). Inert when unset.
const bridged = process.env.REEL_CHROME_BRIDGE;
if (bridged) {
  Config.setBrowserExecutable(path.resolve(bridged));
}
