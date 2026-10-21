# Audio pipeline (`scripts/mix.py`, `recite.py`, `gen_bed.py`, `cues.py`, `tighten.py`)

Default policy for this brand: **no human or synthetic narrator**. Qurʾan recitation when the reel
contains an āyah; otherwise sound design + ambient bed only. Narration is produced only when the user
asks for it explicitly (then it is a *stem* in the spec, see below).

## Spec → mix

```json
"audio": {
  "mode": "silent",                       // silent = text-led (default) | narrated
  "file": "mix.wav",                      // written to <project>/assets/audio/, referenced by <audio>
  "recitation": { "ref": "9:119", "edition": "ar.mahermuaiqly", "at": 3.9 },   // omit when no verse
  "bed": { "gain_db": -7, "duck_db": -9, "fade_out": 2.2, "seed": 7 },        // false → no bed
  "auto_sfx": true,                       // sound design derived from the resolved cues
  "sfx": [ { "name": "chime", "at": 30.4, "gain_db": -16 } ],                 // extra events (optional)
  "stems": [ { "file": "assets/audio/vo-3.wav", "at": 13.4, "gain_db": -1 } ], // narration only on request
  "target_lufs": -15.5, "true_peak_db": -1.5
}
```

`python3 scripts/mix.py <project>` → generates the bed (if any), downloads/trims the recitation (if
`file` missing), lays SFX events, side-chain ducks the bed under the voice bus, masters with a static
gain to the target LUFS + `alimiter` (no one-pass `loudnorm` — it pumps quiet beds). Prints the LUFS
before/after. `--dry-run` prints the event list for review.

## Recitation

`recite.py 9:119 --edition ar.mahermuaiqly --out assets/audio/recite.wav` → trimmed 48 kHz mono WAV,
prints the duration. Budget the verse scene ≥ duration + 1.6 s. Place `at` = the verse scene's first
word cue (mix.py does this automatically when `at` is omitted). Ranges: `2:255-257` (≤ 5 āyāt).
Editions: `ar.mahermuaiqly` (default), `ar.alafasy` (alternative); avoid `ar.husary` (slow),
`ar.abdulsamad`, `ar.parhizgar` (CDN stubs). Some very short āyāt are stubs even for Maher (e.g. 103:1) —
`recite.py` detects clips < 1 s and tells you to switch to `ar.alafasy`. If the download fails (no network), ask the user for a
file and pass `--recitation path`.

Word cues: `cues.py assets/audio/recite.wav --words 8 --offset 3.9 --json` → paste into
`scenes[verse].cues.words`. Listen-check two words (spectrogram or `ffplay`) when possible; adjust by
hand if a word lands early — the eye forgives 100 ms late, never early.

## Sound design vocabulary (auto_sfx; names = files in `assets/sfx/`)

| moment | sound | gain |
|---|---|---|
| every scene cut | `whoosh-short` | −19 dB |
| hook (+0.34) | `whoosh-short` | −24 dB |
| hook emphasis, first verse word, final line | `sparkle` | −19 / −16 / −14 dB |
| verse highlight | `ping` | −24 dB |
| text reveal (labels, lines, attributions) | `click-soft` | −23 dB |
| strike-through | `pen-scratch` | −14 dB |
| right phrase lands, cards, list items | `pop` | −19…−21 dB |
| 6 s before the hero → hero | `riser` (trimmed 4.03 s, 2.5 s fade-in) → `impact-bass-1` | −23 → −14 dB |
| quote hero | `impact-bass-2` | −16 dB |
| seal | `chime` | −16 dB |
| share plane | `whoosh` | −18 dB |

Fewer is better: if a scene has more than one reveal per second, drop its clicks (`"auto_sfx": false`
and list the events you want in `sfx`). `assets/sfx/CREDITS.md` lists sources/licences.

## Bed

`gen_bed.py` synthesises a deterministic D-minor pad + sub drone + soft bells + paper air + synthetic
reverb; chords change on the scene cuts, the brightest voicing lands on the hero cue, bells on the
hero and final cues. −7 dB under everything, ducked −9 dB (ratio 3) under voice/recitation, fades the
last 2.2 s. It is intentionally unobtrusive: a 45 s reel must survive muted autoplay; the bed only has
to make sound-on feel finished.

## Narrated mode (only when asked)

1. Generate voice stems per scene (the platform TTS or a human file), one WAV per scene.
2. `tighten.py in.wav out.wav --max-pause 0.26 --tempo 1.06` removes long internal pauses (ffmpeg's
   `silenceremove` cannot) — Arabic TTS tends to drag.
3. `cues.py out.wav --lines N --offset <scene start>` → line cues; set scene lengths from the stems.
4. Put the stems in `audio.stems` with their `at`; set `"mode": "narrated"`; mix as usual
   (the bed ducks under the voice bus automatically). Target −14 LUFS for narrated reels.
5. Persian narration runs ~20 % longer than Arabic for the same text — rebudget scenes.

## Mastering targets

Integrated −15.5 LUFS (silent mode) / −14 LUFS (narrated), true peak ≤ −1.5 dBTP, 48 kHz. `verify.py
--render` checks the final MP4's loudness.
