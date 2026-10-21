#!/usr/bin/env python3
"""
hook_score_ar.py — score formal-Arabic Reel hooks (0–100) and rank them.

    python3 hook_score_ar.py "هل يكفي الحُبُّ لتكونَ من شيعتِهم؟" "ثلاث صفات تجعلك من شيعتهم" ...
    python3 hook_score_ar.py --file hooks.txt        # one hook per line
    python3 hook_score_ar.py --json content.json     # scores hook.line1 (+line2)

Heuristics adapted from ig-reel/hookscore.py for a dignified, scholarly, Arabic-speaking audience:
curiosity gap, stakes, question form, second person, concrete number, religious specificity
(an Imam / a hadith / a sanad), brevity; penalties for clickbait, slang, emoji, Latin, vagueness.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from _common import EMOJI, LATIN, strip_tashkeel, words

CURIOSITY = ["هل", "لماذا", "كيف", "ما الذي", "ماذا", "أتعلم", "أتدري", "سرّ", "سر ", "حقيقة", "لم يخبرك", "قلّ من", "قليل من", "لا يعرفه", "أخفى", "اختبر"]
STAKES = ["فليس منا", "ليس منا", "لست من", "فلست من", "لن", "خسر", "هلك", "يكفي", "شرط", "لا ينفع", "باطل", "حرام", "لا يقبل", "يوم القيامة", "البرزخ", "الموت", "فقدت", "منهم"]
SECOND_PERSON = ["أنت", "أنتم", "تكون", "تظن", "تعرف", "تحسب", "تحب", "تدعي", "فقدت", "تركت", "تريد", "تعلم", "تدري", "تقرأ", "تصلي"]
SECOND_PERSON_RE = re.compile(r"(^|\s)(ل|ف|و)?(ت\w{2,}|لست)(\s|$)|\w+ك(\s|$|[؟?،.])")  # ت-verbs, لستَ, -ك suffix
SPECIFIC = ["الإمام", "الامام", "النبي", "رسول الله", "الصادق", "الباقر", "الرضا", "الكاظم", "أمير المؤمنين", "علي", "فاطمة", "الحسين", "الحديث", "رواية", "سند", "صحيح", "الشيعة", "شيعت", "القرآن"]
CLICKBAIT = ["لن تصدق", "لن تصدّق", "صادم", "مذهل", "خطير جدا", "كارثة", "فضيحة", "عاجل", "!!!"]
VAGUE = ["شيء", "أمر مهم", "معلومة", "نصيحة", "تأمل", "كلام جميل"]
COLLOQUIAL = ["ليش", "شلون", "وين", "هاي", "هسه", "شنو", "كلش", "خوش"]


def score(hook: str) -> dict:
    raw = hook.strip()
    s = strip_tashkeel(raw)
    n = words(s)
    pts, notes = 0, []

    # Brevity (max 25): sweet spot 4–8 words
    if 4 <= n <= 8:
        pts += 25
    elif n in (3, 9):
        pts += 18; notes.append("length ok-ish (aim 4–8 words)")
    elif n <= 2:
        pts += 8; notes.append("too short to carry a question")
    else:
        pts += max(0, 20 - (n - 9) * 4); notes.append(f"{n} words: too long for 1.5 s reading")

    # Curiosity gap (max 20)
    cur = any(k in s for k in CURIOSITY)
    if cur:
        pts += 14; notes.append("curiosity opener")
    if re.search(r"[؟?]\s*$", s):
        pts += 6; notes.append("question form")
    elif cur:
        pts += 2

    # Stakes / consequence (max 15)
    if any(k in s for k in STAKES):
        pts += 15; notes.append("stakes present")

    # Second person / self-relevance (max 15)
    if any(k in s for k in SECOND_PERSON) or SECOND_PERSON_RE.search(s):
        pts += 15; notes.append("addresses the viewer")

    # Specificity (max 15): an Imam / hadith / number
    sp = any(k in s for k in SPECIFIC)
    num = re.search(r"[٠-٩0-9]|ثلاث|أربع|خمس|سبع|عشر|واحد|اثن", s)
    if sp:
        pts += 9; notes.append("religious specificity")
    if num:
        pts += 6; notes.append("concrete number")

    # Open loop / contrast (max 10)
    if re.search(r"\.\.\.|…|لكن|إلا|ولكن|أم ", s):
        pts += 6; notes.append("open loop / contrast")
    if re.search(r"(يكفي|وحده|فقط)", s):
        pts += 4; notes.append("challenges an assumption")

    # Penalties
    for k in CLICKBAIT:
        if k in s:
            pts -= 25; notes.append(f"clickbait «{k}» — undignified")
    for k in COLLOQUIAL:
        if re.search(rf"(^|\s){k}(\s|$)", s):
            pts -= 30; notes.append(f"colloquial «{k}»")
    if EMOJI.search(raw):
        pts -= 20; notes.append("emoji")
    if LATIN.search(raw):
        pts -= 15; notes.append("Latin letters")
    if any(k in s for k in VAGUE):
        pts -= 10; notes.append("vague wording")
    if raw.count("!") >= 2:
        pts -= 10; notes.append("multiple exclamation marks")
    if n >= 6 and not re.search(r"[\u064B-\u0652]", raw):
        notes.append("tip: add tashkeel on the key word for elegance")

    pts = max(0, min(100, pts))
    grade = "A" if pts >= 80 else "B" if pts >= 65 else "C" if pts >= 50 else "D"
    return {"hook": raw, "words": n, "score": pts, "grade": grade, "notes": notes}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hooks", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--json", help="content.json: score its hook")
    ap.add_argument("--out", help="write ranked JSON here")
    a = ap.parse_args()
    hooks = list(a.hooks)
    if a.file:
        hooks += [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()]
    if a.json:
        c = json.load(open(a.json, encoding="utf-8"))
        h = c["hook"]
        hooks.append((h.get("line1", "") + " " + (h.get("line2") or "")).strip())
    if not hooks:
        ap.error("no hooks given")
    results = sorted((score(h) for h in hooks), key=lambda r: -r["score"])
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['score']:3d} {r['grade']}] {r['hook']}  ({r['words']} w)")
        for n in r["notes"]:
            print(f"      - {n}")
    best = results[0]
    if best["score"] < 65:
        print("\nBest hook is below 65 — rewrite using references/hooks-ar.md formulas before planning.", file=sys.stderr)
    if a.out:
        json.dump(results, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
