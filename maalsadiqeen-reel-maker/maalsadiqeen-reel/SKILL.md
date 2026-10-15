---
name: maalsadiqeen-reel
description: Use when the user wants a reel / short vertical video (ریل، ویدیو، ریلز، reel, Reels) for the Instagram page «مع الصادقين» (@maalsadiqeen, maalsadiqeen), or shares the page's branded Arabic sheets (ورق، پست، پوستر، کارت — cream paper, green arc, tree logo) carrying a verse, ḥadīth, sanad grading, scholar quote, question or occasion and wants them turned into a 30–60 s faceless video — including re-cuts, A/B hooks, 4:5 feed variants, covers, beat sheets, captions, "same style as the Ṣādiqīn reel", or any Arabic religious short-form video in this page's style. Triggers even without an āyah on the sheets and even if the user only asks for a hook, a caption or a QC of an existing cut.
license: Proprietary — made for the maalsadiqeen page; third-party assets per assets/sfx/CREDITS.md and font licences (OFL).
metadata:
  title: Maalsadiqeen Reel Maker — ریل‌ساز مع الصادقین
  version: 2.0.1
  brand: maalsadiqeen
  output: 1080x1920 MP4 (30 fps, ≤60 s) + cover + beat sheet + post kit
  requires: python3 ≥3.9 (numpy, pillow), ffmpeg/ffprobe, node ≥22 + hyperframes 0.8.x (default engine) — or node + remotion 4 (alternate engine)
---

# Maalsadiqeen Reel Maker (`maalsadiqeen-reel`) — from the page's sheets to a finished reel

Turn one or more branded sheets of «مع الصادقين» into a dignified, text-led, viral-ready vertical video:
read the sheets, decide the story, write فصيح Arabic copy, compile a project from a JSON spec, build the
soundtrack (recitation + sound design, no narrator), verify with snapshots, render, and hand over master +
cover + beat sheet + post kit with a Persian summary. Everything the generic video / motion / Reels skills
taught for this page is encoded here as scripts and references — do not re-derive it.

## Non-negotiables

1. **No human or synthetic narrator** unless the user asks for one in this conversation. Qurʾan recitation
   is welcome when the reel contains an āyah. The reel must make full sense muted.
2. **≤ 60 s, 9:16 1080×1920, 30 fps**; default length 45 s (36–50 s window).
3. **Brand = paper, green, gold** (`references/brand.md`, the single source of truth for both engines).
   No new colours, fonts or effects; never red.
4. **Copy is فصيح, متين, fully vocalised** where sacred/quoted (`references/arabic-copy.md`). Never alter
   or "repair" a verse/ḥadīth from memory; quote the sheet, flag unreadable spots to the user.
5. **No invented references or gradings.** No source on the sheet → no proof block (say so).
6. **`verify.py` must pass before rendering** and the snapshots must be looked at with your own eyes.
7. Reply to the user in Persian; on-screen copy in Arabic (Persian only if explicitly requested).

## Engines — one skill, one default

| engine | when | entry |
|---|---|---|
| **HyperFrames** (default) | everything: verse + ḥadīth, ḥadīth only, concept, FAQ, occasion, objection | this file |
| Remotion studio (alternate) | ḥadīth + numbered traits + long rijāl chain carousels (animated chain, «ثقة» stamps, seal); user already has `~/reel-studio` or asks for Remotion; HyperFrames cannot run | `references/remotion-studio.md` + `remotion-schema.md` |

Both engines share the brand, the copy rules, the hook scorer, the post kit and the loudness target.
Do not mix them inside one reel.

## Workflow (HyperFrames engine)

All paths come from `scripts/env.sh`: `$SKILL_DIR` (this folder), `$REEL_WORK` (projects, default
`./reel-work`), `$REEL_DELIVER` (finished files, default `./reel-deliver`), `$HF_WORKDIR` (where
`node_modules/hyperframes` lives, default `~/reel-sadiqeen`). Override any of them before sourcing.

### 0 · Toolchain (every session on an ephemeral machine)

```bash
source <path-to-this-skill>/scripts/env.sh          # prints missing pieces + exact install commands
S="$SKILL_DIR/scripts"; W="$REEL_WORK/<slug>"; D="$REEL_DELIVER"; mkdir -p "$W"
```
Fix whatever it reports (`references/troubleshooting.md`). Never run two renders or checks at once.

### 1 · Read the sheets → brief (`references/content-analysis.md`)

Open every attached image. Transcribe sacred text, references, scholar comments, the page's framing.
Classify (A verse+ḥadīth+grading · B ḥadīth only · C scholar/concept · D FAQ · E occasion · F objection)
and write the one-sentence idea, hinge word, surprise, authority, take-away → `$W/brief.md`. If the sheets
hold two ideas, propose two reels. Research briefly only when it adds value (verifying a reference, a
recitation choice); cite it in the brief. Do not scrape Instagram.

### 2 · Hook, then scenario = spec (`references/hooks-ar.md`, `narrative.md`, `blocks.md`)

```bash
python3 $S/hook_score_ar.py "hook 1" "hook 2" "hook 3" --out $W/hooks.json   # one question, one number/condition, one stakes hook; best ≥ 65 (aim ≥ 80)
python3 $S/new_spec.py --archetype A --duration 45 --out $W/spec.json [--recitation 9:119]
```
Replace every «…» in the spec with final copy. Rules of thumb: hook word on screen by 1.2 s; at most one
`<em>` hinge word per line; ≤ 70 words on screen in total; one hero line; CTA ≥ 6.4 s with
«أَرْسِلْهَا لِمَنْ تُحِبّ» and the brand card. Keep explicit `cues` only where the audio dictates them
(verse words); otherwise let the builder pace by reading speed.

With a verse, fetch the recitation first and size the verse scene from it:
```bash
python3 $S/recite.py 9:119 --out $W/recite.wav       # prints duration → verse scene ≥ duration + 1.6 s; offline: --from-files a.mp3
python3 $S/cues.py $W/recite.wav --words 8 --offset <verse scene start> --json   # → scenes[verse].cues.words
```

### 3 · Build

```bash
python3 $S/build_reel.py $W/spec.json --out $W/project    # → index.html + spec.resolved.json; read every WARN
```
Fix WARNs by editing the spec, never the generated HTML (except a one-off last resort).

### 4 · Soundtrack (`references/audio.md`)

```bash
cp $W/recite.wav $W/project/assets/audio/recite.wav 2>/dev/null; python3 $S/mix.py $W/project --dry-run   # review the event list
python3 $S/mix.py $W/project        # bed + recitation + auto sound design → assets/audio/mix.wav, prints LUFS (target −15.5)
```
Narration only on explicit request: produce stems, `tighten.py`, add them to `audio.stems`, `mode: narrated`.

### 5 · Verify — the pre-render gate (`references/qc.md`)

```bash
python3 $S/verify.py $W/project     # pacing · html · hyperframes check · snapshots → qc/sheet.jpg (exit 1 on any FAIL)
```
Open `$W/project/qc/sheet.jpg`. Check typography, clipping, gold emphasis, seal, watermark, brand card.
Iterate spec → build → mix → verify until 0 failures and the frames look right. If the cover frame
(hero + 0.9 s) would not stop a scroll, rewrite the hero/hook now, not after rendering. When the user is
in the loop, show the sheet and ask "render now, or what changes?" — unless they asked for a finished file
without review.

### 6 · Render (3.5–6 min, background process)

```bash
bash $S/render.sh $W/project $D/<slug>.mp4                        # check → render --workers 1 → ffprobe; one render at a time
python3 $S/verify.py $W/project --render $D/<slug>.mp4 --no-check  # 1080×1920 · 30 fps · duration · AAC · LUFS · true peak
```
Grab 4–6 frames from the MP4 with ffmpeg and compare them to the snapshots (a blank render = `dir=rtl`
on `<html>` or missing fonts).

### 7 · Deliverables (`references/publish.md`)

```bash
python3 $S/export_variants.py $D/<slug>.mp4 --out $D --name <slug> --spec $W/project/spec.resolved.json [--feed] [--audio]
python3 $S/beat_sheet.py $W/project --spec $W/spec.json --out $D/<slug>-beat-sheet.md --lang fa
python3 $S/post_kit.py $W/spec.json --hooks $W/hooks.json -o $D/<slug>-post.md      # caption · pinned references · alt hooks · checklist
```
Present the MP4. In the Persian summary give: idea + archetype, the scene table (time, copy, source),
audio plan, what was verified (check / snapshots / LUFS / duration), posting advice (cover, caption,
A/B or Trial Reels, metrics to watch) and every flagged uncertainty (unreadable word, missing reference).

## Decision points

| situation | do |
|---|---|
| sheets contain an āyah | archetype A (or E); recitation `ar.mahermuaiqly`; verse words cued from `cues.py` |
| no āyah, a ḥadīth with reference | B; `quote` with `reveal: words`; proof cards without seal unless a grading is stated |
| only a scholar's point / concept | C; the contrast block carries the turn; hero = the text that settles it |
| question-type sheet | D; answer as `list` (≤ 3) or `quote`; keep the answer scene ≥ 8 s |
| date / person / occasion | E; `title` card first; no contrast; final = greeting line |
| objection / شبهة | F; calm tone, quote the objection neutrally, never name opponents |
| ḥadīth + numbered traits + long chain carousel | consider the Remotion engine (`references/remotion-studio.md`) |
| user asks for narration | narrated mode: stems + `tighten.py` + `cues.py --lines`; target −14 LUFS; Persian runs 20 % longer |
| user asks for a variant | A/B: change scene 1 only; feed: `export_variants.py --feed`; Persian version: translate copy, shrink sizes / `nowrap` |
| user wants > 60 s | decline politely; propose a two-part series with the same opening signature |
| toolchain missing / render impossible | still deliver brief + spec + beat sheet + post kit (+ snapshots if `check` runs) and the exact commands that remain |

## Files

| path | purpose |
|---|---|
| `scripts/env.sh` | paths (`SKILL_DIR`, `REEL_WORK`, `REEL_DELIVER`, `HF_WORKDIR`) + toolchain check — source it first |
| `scripts/hook_score_ar.py`, `scripts/post_kit.py`, `scripts/extract_brand.py` | shared tools (both engines): Arabic hook scoring; caption / pinned comment / checklist; palette + logo extraction from a card |
| `scripts/new_spec.py`, `scripts/build_reel.py` | archetype scaffolds A–F; spec → HyperFrames project (blocks hook, verse, contrast, answer, proof, cta, quote, list, title; Arabic font fitting; reading-speed cues) |
| `scripts/recite.py`, `scripts/cues.py` | recitation download/trim (or `--from-files`); word/line onset detection |
| `scripts/mix.py`, `scripts/gen_bed.py`, `scripts/tighten.py` | soundtrack: bed, recitation, auto sound design, ducking, mastering; narration tightening |
| `scripts/verify.py`, `scripts/render.sh` | QC gates (pre/post render); check + render wrapper |
| `scripts/export_variants.py`, `scripts/beat_sheet.py` | cover, 4:5, 1:1, audio stem; Persian/Arabic/English beat sheet |
| `scripts/setup_studio.py`, `validate_content.py`, `plan.py`, `make_audio.py`, `render.py` | Remotion engine only (see `references/remotion-studio.md`) |
| `references/brand.md` | tokens, typography, grid, motion personality, tone — for both engines |
| `references/content-analysis.md` | reading the sheets, classification, brief template |
| `references/hooks-ar.md`, `references/narrative.md` | 12 Arabic hook formulas + scoring routine; archetypes A–F with timings; A/B rules |
| `references/arabic-copy.md`, `references/blocks.md` | register, quoting, tashkeel checklist, line budgets; spec format and every block's fields and cues |
| `references/audio.md`, `references/motion.md` | soundtrack design rules; HyperFrames/GSAP rules and choreography |
| `references/qc.md`, `references/publish.md`, `references/troubleshooting.md` | gates & defects; posting playbook, anti-patterns, cold start, flop diagnosis; toolchain fixes |
| `references/remotion-studio.md`, `references/remotion-schema.md` | the alternate engine: workflow, design tokens, QA checklist; `content.json` / `plan.json` schema |
| `assets/examples/` | `sadiqeen-9-119.silent.json` (archetype A, the delivered 45 s reel — gold standard), `hadith-only.json` (B/C, 41 s), contact sheets, beat sheet; `shiatuna/`, `variant-bayan/` for the Remotion engine |
| `assets/{fonts,brand,sfx,gsap.min.js,hyperframes.json}` | everything `build_reel.py` copies into a project; `assets/remotion-template/` is the Remotion studio |
| `evals/evals.json`, `evals/rubric.md`, `evals/files/` | 5 test prompts (2 need the page's private sheets — see `evals/files/README.md`) + grading rubric |

## Done means

- `$REEL_DELIVER/<slug>.mp4` passes `verify.py --render` (1080×1920, ≤ 60 s, AAC, LUFS within ±1.2 of target).
- `<slug>-cover.jpg`, `<slug>-beat-sheet.md`, `<slug>-post.md` exist next to it.
- Snapshots were inspected; every quoted text matches the sheets; every reference comes from the sheets.
- The Persian summary states what was built, what was verified, and what the user should check.
