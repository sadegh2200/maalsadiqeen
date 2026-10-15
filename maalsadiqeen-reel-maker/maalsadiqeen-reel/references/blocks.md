# Spec format & block library (`scripts/build_reel.py`)

A reel is a JSON spec: metadata + `audio` + an ordered list of `scenes`. Each scene is one block type.
`build_reel.py spec.json --out <project>` compiles it to a HyperFrames project and writes
`spec.resolved.json` with every cue in absolute seconds (consumed by `mix.py` and `verify.py`).

```json
{
  "id": "slug", "title": "…", "duration": 45,
  "brand": { "handle": "maalsadiqeen" },
  "watermark": { "show": true },               // optional: "from"/"until" seconds
  "audio": { … see audio.md … },
  "scenes": [ { "id": "s1", "type": "hook", "start": 0, "end": 3.4, … }, … ]
}
```

Rules enforced/derived by the builder:
- Scenes are contiguous (`end` of one = `start` of next; `end` may be omitted). Last `end` = `duration`.
- `cues` are optional. Omitted cues come from reading-speed defaults (1.15 s + 0.26 s/word per line,
  0.18 s gap). Given cues may be absolute seconds or relative strings `"+1.2"` (from scene start).
- Font sizes are fitted per line with exact Arabic shaping (Pillow+raqm), capped at the brand ranges.
- `<em>…</em>` inside any text field = gold emphasis. Plain `<`/`&` are escaped automatically.
- Warnings print as `WARN …` — treat "last reveal < 0.9 s before scene end" as a real problem.

## hook — the first 3–4 s

| field | role |
|---|---|
| `lead` (+ `lead_font` quran\|amiri) | quoted fragment, 0.92 opacity, small |
| `line1` | kufi, e.g. «فَمَنْ هُمُ» |
| `line2` | the big word(s) with gold underline bar, kufi ≤ 138 px |
| `sub` | naskh, source line |
| `cues.emphasis` | underline + pulse moment (default min(end−1.2, start+1.9)) |

Lead appears at +0, line1 +0.16, line2 +0.34, rule +0.85, sub +1.0.

## verse — Qurʾanic text revealed word by word

| field | role |
|---|---|
| `label` | «﴿ سُورَةُ … — ١١٩ ﴾» (kufi-r gold) |
| `lines` | list of word-lists; forced breaks between lists, natural wrap inside |
| `font` | `quran` (default) or `amiri`; `size` to force px; `nowrap: true` to forbid wrapping; `max_lines` (4) |
| `highlight` | `{ "words": [7, 8], "at": 11.0 }` 1-based word indices turned gold+1.05 |
| `cues.words` | absolute onset per word (from `cues.py`); default = evenly paced |

Words animate in 0.28 s before their cue (blur+rise) so the word is fully readable on the beat.

## contrast — strike the wrong reading, light the right one

`wrong_label`, `wrong` (struck), `right_label`, `right` (with `<em>`), `line3` (kufi), `line4` (naskh,
its `<em>` turns gold later). Cues: `wrong`, `strike`, `right`, `line3`, `line4`, `line4_gold`.

## answer — the hero moment

`q1` (amiri), `q2` (naskh), `hero` (amiri bold ≤ 118 px, wipe + gold underline + glow + camera push),
`after` (amiri), `source` (naskh). Cues: `q1`, `q2`, `hero`, `after`, `source`.

## proof — authority

`seal`: `["صَحِيحُ", "السَّنَد"]` or omit when no grading. `cards`: up to 3 `{book, loc, grade}`.
`line1`/`line2` (amiri bold; line2 gold), `attribution`. Cues: `seal`, `cards` (list), `line1`,
`line2`, `attribution`.

## cta — take-away + share + brand

`line1` (kufi, with drawn gold path under it), `line2` (amiri + `<em>`), `share` (plane icon + text),
`final` (+ `final_font`, default quran, gold rule under it), `brand.handle`. Cues: `line1`, `line2`,
`share`, `final`, `brand` (default final+0.7). The arc divider fades out at scene start + 0.2.

## quote — generic ḥadīth / scholar text

`label`, `text` (string or list of lines), `reveal: "lines"|"words"`, `font` (amiri default), `hero: true`
(underline + glow + push), `attribution`, `size`, `max_lines`. Cues: `lines` or `words` (lists),
`attribution`, `hero`.

## list — ≤ 4 short items

`title` (kufi), `items` (naskh, auto-numbered with Arabic-Indic digits unless `numbered: false`),
`attribution`. Cues: `title`, `items` (list), `attribution`.

## title — occasion / section card

`kicker` (kufi-r gold), `title` (kufi ≤ 110 px with gold rule), `sub` (naskh). Cues: `kicker`, `title`, `sub`.

## Timing recipes

- Scene length for a `verse` = recitation duration + 1.6 s (+0.8 s if a label is used).
- `answer`: hero at ≈ start + 3.0 s; scene ≥ 8 s so the hero holds ≥ 4 s.
- `proof`: 1 card → 7.5 s; 2 cards → 9 s; 3 cards → 10.5 s.
- `cta`: 6.4 s minimum (brand card needs 1.5 s alone).

## Extending the library

Add a `blk_<name>(sc, ctx)` function in `build_reel.py` that appends HTML to `ctx.html`, GSAP calls to
`ctx.js`, cues to `ctx.cues[sid]`, and register it in `BLOCKS`. Reuse `enter/exit/heroIn/drawPath`
helpers; keep CSS class-scoped under `.blk-<name>`; never animate `#root` or set `dir` on `<html>`.
Then add an example spec under `assets/examples/` and an eval that uses it.
