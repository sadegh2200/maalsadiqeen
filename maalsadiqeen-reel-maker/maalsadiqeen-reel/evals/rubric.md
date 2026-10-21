# Grading rubric — maalsadiqeen-reel v3

Score each line 0–2 (0 missing, 1 partial, 2 fully met). A run passes at **≥ 85 %** with **no 0 in a ★
line**. Compare two runs by asking: which one would the page publish?

## The gate (new in v3 — a run fails here first)

| # | criterion | ★ |
|---|---|---|
| 1 | The agent produced **four complete scenarios** (hook, scenes, sources, life_impact, why_fa) before building | ★ |
| 2 | The four use at least three distinct angles and two archetypes; none is filler | |
| 3 | `scenarios.py` validation passes and the plan is scored and shown as a Persian table with a preview | |
| 4 | **Nothing was built or rendered before the user chose** — «بساز» is answered with a plan, not an MP4 | ★ |
| 5 | The chosen scenario is the one built, unchanged; if the user asked for changes, the plan was re-finalised | |

## Input and identity

| # | criterion | ★ |
|---|---|---|
| 6 | The input is read faithfully (images opened or text read), sacred text transcribed verbatim, never from memory | ★ |
| 7 | The three layers are visibly distinct: نصّ with ﴿﴾/book-page, شرح with a named scholar, استنباط marked as ours | ★ |
| 8 | An «الأثر في الحياة» line exists — one concrete deed, 4–32 words, no slogan | ★ |
| 9 | No invented reference, page or grading; no seal without a stated grading | ★ |
| 10 | The objection/refutation (if any) is fair and names no sect, group or opponent | |
| 11 | Honorifics present for every Maʿṣūm named on screen | |

## Copy and kit

| # | criterion | ★ |
|---|---|---|
| 12 | Copy is فصيح, vocalised where sacred/quoted, ≤ 70 on-screen words, no dialect/emoji/«!»/Latin | |
| 13 | Hooks scored with `hook_score_ar.py`; nothing offered below 65 (best ≥ 80 preferred) | |
| 14 | Three captions inside the platform limits, no links in body, no follow-bait | ★ |
| 15 | Seven comments, ≤ 300 chars, the first pinned with the reference, scheduled in local + UTC | |
| 16 | `validation.md` green; a red caption is moved aside, not shipped | |

## Build and sound

| # | criterion | ★ |
|---|---|---|
| 17 | `build_reel.py` used, every WARN read; cues sane (hook ≤ 4.5 s, one hero, CTA ≥ 6.4 s) | |
| 18 | No narrator unless requested; recitation only when an āyah is on screen; verse sized from the recitation | ★ |
| 19 | `mix.py` used; target −15.5 LUFS reported; a missing recitation is flagged, never hidden | |
| 20 | `verify.py` pre-render passes and `qc/sheet.jpg` was actually inspected | ★ |
| 21 | Render is 1080×1920, 30 fps, 30–60 s, AAC; `verify.py --render` passes | ★ |
| 22 | A missing toolchain is reported honestly: no invented MP4, no invented LUFS, exact next commands given | ★ |

## Delivery and voice

| # | criterion | ★ |
|---|---|---|
| 23 | Deliverables are the requested preset (minimal / standard / full); no cover unless asked | |
| 24 | Files land in `$REEL_DELIVER/<slug>-<id>/` with the kit; names consistent | |
| 25 | The Persian summary gives the scene table, what was verified, what to check, and when to post | |
| 26 | Brand fidelity in frames: paper/green/gold, arc + sprig, watermark, brand card ≥ 1.5 s, nothing clipped | |

## How to compare runs

Prefer the run that: **stopped at the gate** when it should have, shipped a verified reel with faithful
quotes, and said out loud what it could not verify. Penalise, in this order:

1. inventing a reference, a grading or a render;
2. building before the user chose;
3. a narrator or a dialect/emoji line that the brand forbids;
4. a red kit shipped as if it were green;
5. visual flaws.
