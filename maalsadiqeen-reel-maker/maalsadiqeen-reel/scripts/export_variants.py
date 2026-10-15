#!/usr/bin/env python3
"""
export_variants.py — derive the publishing set from a rendered 9:16 master.

    python3 export_variants.py master.mp4 --out deliver/ --name sadiqeen-9-119 [--cover 24.9] [--feed] [--square] [--audio]

  cover   → <name>-cover.jpg      frame at the strongest beat (default: hero cue + 0.9 s from spec.resolved.json if --spec given)
  --feed  → <name>-feed-4x5.mp4   1080×1350 crop of the safe zone (crop=1080:1350:0:220) for the feed grid
  --square→ <name>-1x1.mp4        1080×1080 (crop y 420) for carousels / WhatsApp
  --audio → <name>.m4a            AAC 192k stem (for reuse / Trial Reels re-upload)
Also writes <name>-caption.txt skeleton if --caption is given (text file to paste).
"""
import argparse, json, os, subprocess, sys


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-2000:]); raise SystemExit("ffmpeg failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master"); ap.add_argument("--out", default="deliver"); ap.add_argument("--name", default=None)
    ap.add_argument("--spec", help="spec.resolved.json (to pick the cover time automatically)")
    ap.add_argument("--cover", type=float, default=None); ap.add_argument("--feed", action="store_true")
    ap.add_argument("--square", action="store_true"); ap.add_argument("--audio", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    name = a.name or os.path.splitext(os.path.basename(a.master))[0]
    t = a.cover
    if t is None and a.spec:
        res = json.load(open(a.spec, encoding="utf-8"))
        for sc in res["scenes"]:
            if sc["type"] in ("answer", "quote") and isinstance(sc["cues"].get("hero"), (int, float)):
                t = sc["cues"]["hero"] + 0.9; break
    if t is None:
        t = 1.6  # hook with the big line fully in
    cover = os.path.join(a.out, f"{name}-cover.jpg")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t), "-i", a.master, "-frames:v", "1", "-q:v", "2", cover])
    print("cover", cover, f"@{t}s")
    enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k"]
    if a.feed:
        p = os.path.join(a.out, f"{name}-feed-4x5.mp4")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.master, "-vf", "crop=1080:1350:0:220"] + enc + [p]); print("feed 4:5", p)
    if a.square:
        p = os.path.join(a.out, f"{name}-1x1.mp4")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.master, "-vf", "crop=1080:1080:0:420"] + enc + [p]); print("square", p)
    if a.audio:
        p = os.path.join(a.out, f"{name}.m4a")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.master, "-vn", "-c:a", "aac", "-b:a", "192k", p]); print("audio", p)


if __name__ == "__main__":
    main()
