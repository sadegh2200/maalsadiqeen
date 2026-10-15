# Grading rubric — maalsadiqeen-reel

Score each eval 0–2 per line (0 missing, 1 partial, 2 fully met). A run "passes" at ≥ 85 % with no 0 in a ★ line.

| # | criterion | ★ |
|---|---|---|
| 1 | Sheets were actually read (images opened) and sacred text/references transcribed verbatim, not from memory | ★ |
| 2 | Correct archetype chosen and justified in one sentence (hinge word, surprise, authority) | |
| 3 | No narrator unless requested; recitation only when an āyah is on screen | ★ |
| 4 | No fabricated references or gradings; proof block dropped when the sheet has none | ★ |
| 5 | Copy is فصيح, vocalised where quoted, ≤ 70 words, no exclamation/emojis/dialect | |
| 6 | Spec built with `build_reel.py`; WARNs resolved; cues sane (hook ≤ 4.5 s, hero 50–65 %, CTA ≥ 6.4 s) | |
| 7 | `mix.py` used; LUFS printed within ±0.5 of target; event list reviewed | |
| 8 | `verify.py` pre-render passed and `qc/sheet.jpg` was opened and commented on | ★ |
| 9 | Render 1080×1920 / 30 fps / 30–60 s / AAC; `verify.py --render` passed | ★ |
| 10 | Deliverables: MP4 + cover + beat sheet (+ caption); Persian summary with scene table, verification results, posting advice | |
| 11 | Brand fidelity in frames: paper/green/gold, arc + sprig, watermark, brand card ≥ 1.5 s, nothing clipped | |
| 12 | Honest flags: unreadable words, missing references, toolchain limits, anything the user must check | |

Comparison between runs (with/without skill): prefer the run that ships a verified MP4 with faithful
quotes; penalise any invented source or any narrator track more than any visual flaw.
