#!/usr/bin/env bash
# chrome-bridge.sh — let Remotion drive a self-managed headless-shell binary.
#
# Use when the machine cannot download Chrome-for-Testing (offline sandbox, CI behind a proxy,
# `npx remotion browser ensure` blocked). Remotion only needs an executable that accepts its
# flags; any recent chrome-headless-shell / Chromium build works.
#
#   1) get a binary, e.g. the portable build that ships with the @sparticuz/chromium npm package
#        cd <studio> && npm install --no-save --package-lock=false @sparticuz/chromium
#        node --input-type=module -e "import c from '@sparticuz/chromium'; console.log(await c.executablePath())"
#      (it unpacks the binary to \$TMPDIR/chromium and, if the distro is not Amazon Linux 2023,
#       extract node_modules/@sparticuz/chromium/bin/al2023.tar.br next to it for libnss3/libnspr4)
#   2) point the bridge at your binary and export the env var the Remotion config reads:
#        export REEL_BROWSER=/tmp/chromium
#        export REEL_BROWSER_LIBS=/tmp/al2023/lib      # optional, extra LD_LIBRARY_PATH entries
#        export REEL_CHROME_BRIDGE=$PWD/chrome-bridge.sh
#        npx remotion render src/index.ts Reel out/reel.mp4
#
# The flags below are the ones a headless shell needs in a container without a GPU;
# keep --no-sandbox only in trusted, single-tenant environments such as a CI sandbox.
set -euo pipefail

BROWSER="${REEL_BROWSER:-/tmp/chromium}"
LIBS="${REEL_BROWSER_LIBS:-}"
if [ -n "$LIBS" ]; then
  export LD_LIBRARY_PATH="$LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

exec "$BROWSER" \
  --no-sandbox --no-zygote --single-process \
  --in-process-gpu --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --ignore-gpu-blocklist --enable-features=SharedArrayBuffer \
  --disable-features=AudioServiceOutOfProcess,IsolateOrigins,site-per-process \
  --disable-setuid-sandbox --disable-dev-shm-usage --disable-gpu-sandbox \
  --headless='shell' --hide-scrollbars --mute-audio --no-first-run \
  --disable-background-timer-throttling --disable-backgrounding-occluded-windows \
  --disable-renderer-backgrounding --disable-ipc-flooding-protection \
  --force-color-profile=srgb --font-render-hinting=none \
  "$@"
