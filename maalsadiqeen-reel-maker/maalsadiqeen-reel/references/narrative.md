# Narrative archetypes & beat sheets (30–60 s, default 45 s)

Every reel has the same spine — **hook → evidence → turn → authority → proof → take-away/CTA** —
but the blocks and timings change with the content class. Scene budgets below are for 45 s; scale
proportionally for 36–58 s, never beyond 60 s (verify.py fails at > 60).

Universal pacing rules (validated on the delivered reels):
- First cut ≤ 4.5 s; the big hook word is on screen by 1.2 s.
- Each text line gets ≥ 1.15 s + 0.26 s/word before the next reveal (`build_reel.py` default).
- No frame is static for > 3.4 s. A verse scene must be ≥ recitation length + 1.6 s.
- One hero moment (the answer) between 50–65 % of the runtime — it is the frame people screenshot.
- Last 6–7 s = CTA: take-away line + share line + brand card; brand card visible ≥ 1.5 s.

## A · سؤال → جواب المعصوم (verse + ḥadīth + grading) — 45 s, six scenes

| # | block | s | content | cues |
|---|---|---|---|---|
| 1 | hook | 0–3.4 | lead = the verse fragment «…»; line1 «فَمَنْ هُمُ»; line2 the subject with «؟»; sub = sūrah · āyah | emphasis 1.9 |
| 2 | verse | 3.4–13.2 | full āyah word-by-word synced to recitation; highlight the hinge words at the end | words from `cues.py`, highlight ≈ last word + 0.6 |
| 3 | contrast | 13.2–21.6 | «الأَمْرُ لَيْسَ: …» (strike) / «بَلْ: … <em>hinge</em> …» / consequence line / consequence 2 with `<em>` | wrong +0.3, strike +1.4, right +2.4, line3 +4.2, line4 +5.4 |
| 4 | answer | 21.6–29.6 | q1 «سُئِلَ الإمَامُ … عَلَيْهِ السَّلام», q2 «عَنْ هَذِهِ الآيَة… فَقَالَ:», hero = the decisive sentence, after = its second clause, source | hero ≈ +3.0 |
| 5 | proof | 29.6–38.6 | seal «صَحِيحُ / السَّنَد», 1–2 cards (book · ج/ص · grading), scholar line1/line2, attribution | seal +0.8, cards +2.0/+3.1 |
| 6 | cta | 38.6–45 | line1 (2–3 words), line2 with `<em>`, share «أَرْسِلْهَا لِمَنْ تُحِبّ», final = the verse fragment, brand | final ≈ end − 2.3 |

Example: `assets/examples/sadiqeen-9-119.silent.json` (the delivered reel).

## B · كلمة واحدة تغيّر المعنى (a ḥadīth whose meaning turns on one word) — 42 s

1. **hook** (0–3.4): lead = 3–4 words of the ḥadīth; line1 «مَاذَا تَعْنِي»; line2 the hinge word «…؟».
2. **quote** (3.4–12): the ḥadīth, `reveal: "words"`, label «قَالَ الإمَامُ … عَلَيْهِ السَّلام», attribution.
3. **contrast** (12–20): wrong reading (strike) vs right reading with `<em>hinge</em>` + consequence.
4. **quote** `hero: true` (20–28): the decisive clause alone, 1–2 lines, big; attribution with ج/ص.
5. **proof** (28–36): seal if graded; cards; scholar line(s).
6. **cta** (36–42).
Without a verse there is no recitation → `audio.recitation` omitted; sound design + bed only.

## C · تصحيح مفهوم (correcting a common notion) — 40 s

1. **hook**: line1 «يَظُنُّ كَثِيرُون» / line2 the notion «…»; sub «وَالنَّصُّ يَقُولُ غَيْرَ ذَلِك».
2. **contrast**: the notion (strike) vs the text's wording (`<em>`), then «الفَرْقُ: …».
3. **quote** (`hero: true`): the text that settles it.
4. **list** (optional, 3 items max): what follows from the correction.
5. **proof** (cards only, no seal unless a graded ḥadīth).
6. **cta**.

## D · سؤال → جواب (FAQ) — 36–45 s

hook (the question, line2 = the 1–2 word core) → **title** «الجَوَاب» kicker + 1 line → **quote** or
**list** (the answer, ≤ 3 items) → **proof** (one card) → **cta**. Keep the answer scene ≥ 8 s.

## E · مناسبة (occasion) — 30–36 s

**title** (kicker = date «١٣ رجب», title = the name/occasion, sub = one line) → **quote** (`reveal:
"words"`, one ḥadīth or verse about the person/occasion, with recitation if a verse) → **quote** `hero`
(the one line to remember) → **cta** (final = greeting line, e.g. «عَظَّمَ اللهُ أُجُورَكُم» /
«مُبَارَكٌ عَلَيْكُم»). No contrast block — occasions are not arguments.

## F · ردّ شبهة (answering an objection) — 45–50 s

hook (state the objection as a quoted question, calmly) → **contrast** (objection struck, the text's
actual claim in gold) → **quote** hero (the decisive text) → **proof** (cards + scholar) → **list**
(2–3 short consequences, optional) → **cta** (final = the sacred text, never a jab).

## Hook formulas that fit this brand (from the ig-reel skill, filtered for dignity)

The full table of 12 formal-Arabic formulas, the writing rules and the three-hook routine are in
`hooks-ar.md`; score candidates with `scripts/hook_score_ar.py` (publish ≥ 65, aim ≥ 80). The short list:

| formula | pattern | example |
|---|---|---|
| Open question on a known text | «‹قطعة من النص› … فَمَنْ/فَمَا/فَلِمَاذَا …؟» | «كُونُوا مَعَ الصَّادِقِينَ» … فَمَنْ هُمُ الصَّادِقُون؟ |
| Condition → consequence | «إِذَا كَانَ … فَـ…؟» | إِذَا كَانَتِ التَّقْوَى فَرِيضَة، فَمَعَ مَنْ أَمَرَكَ اللهُ أَنْ تَكُون؟ |
| One word | «كَلِمَةٌ وَاحِدَةٌ تُغَيِّرُ المَعْنَى» + the word | كَلِمَةٌ وَاحِدَة: مَعَ |
| Common assumption | «يَظُنُّ كَثِيرُونَ أَنَّ …» | يَظُنُّ كَثِيرُونَ أَنَّ الصِّدْقَ صِفَةٌ فَقَط |
| Count | «ثَلَاثَةُ أُمُورٍ …» (only when the text itself counts) | ثَلَاثٌ لَا يُغْفَرْن |
| Direct address | «أَنْتَ مَأْمُورٌ بِـ…» | أَنْتَ مَأْمُورٌ أَنْ تَكُونَ مَعَ أُنَاسٍ بِأَعْيَانِهِم |

Rejected formulas (clash with the brand): "nobody tells you this", "stop doing X", shock numbers,
countdown bait, anything that implies the audience is ignorant.

## A/B variants

Produce a second hook when asked (or when the first is a plain question): change only scene 1's
text (keep length), re-run build/mix/verify, render, post 3–4 days apart or as Trial Reels; judge
by average watch time and sends/reach (publish.md).
