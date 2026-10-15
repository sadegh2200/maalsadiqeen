#!/usr/bin/env python3
"""
make_beat_sheet.py — Persian beat sheet for the Remotion-engine reel.

The bundled scripts/beat_sheet.py is the HyperFrames-engine tool: it reads the builder's
`spec.resolved.json` (which the Remotion engine does not produce) and its audio-event block comes
from `mix.py`. This small adapter does the same job for the alternate engine: it joins
`content.json` + `plan.json` into the same Persian scene table (time · copy · source · cues), using
`plan.sfx` for the audio-event list, so the deliverable set stays identical in both engines.

    python3 make_beat_sheet.py --content content.json --plan plan.json --out beat-sheet.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def sec(frames: int, fps: int) -> str:
    return f"{frames / fps:.1f}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--content", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    c = json.load(open(a.content, encoding="utf-8"))
    p = json.load(open(a.plan, encoding="utf-8"))
    fps, total = p["fps"], p["total"]
    s = p["scenes"]
    row = lambda sid, copy, src: (
        f"| {sid} | {sec(s[sid]['from'], fps)}–{sec(s[sid]['from'] + s[sid]['dur'], fps)} "
        f"({s[sid]['dur'] / fps:.1f}s) | {copy} | {src} |"
    )

    hd = c["hadith"]
    hadith_src = "وسائل الشيعة ج٤ ص٥٧ · صفات الشيعة ج١ ص٢ · بحار الأنوار ج٦٥ ص١٦٧"
    bay = c.get("bayan") or {}
    san = c.get("sanad") or {}

    lines = [
        f"# بیت‌شیت ریل — {c.get('title', c.get('slug', ''))}",
        "",
        f"- مدت: **{total / fps:.1f} ثانیه** ({total} فریم، {fps} fps) · ۱۰۸۰×۱۹۲۰ · موتور Remotion",
        f"- حالت صدا: `bed + sfx` (بدون گوینده؛ بستر بی‌ضربِ مقام بیات + افکت‌های کاغذ/نوشتار)",
        "- متن روی تصویر: عربی فصیح با اعراب؛ واژهٔ برجستهٔ قلاب در همان سطر مشخص شده است.",
        "",
        "| صحنه | زمان | متن روی تصویر | منبع |",
        "|---|---|---|---|",
        row(
            "hook",
            f"**{c['hook']['line1']} {c['hook']['line2']}** — زیرنویس: {c['hook'].get('sub', '')}"
            f" (واژهٔ برجسته: {c['hook'].get('highlight', '—')})",
            "قلاب تدوینی؛ برگرفته از موضوع بطاقه‌ها",
        ),
        row(
            "hadith",
            f"مقدمه: {hd.get('intro', '')}<br>" + "<br>".join(x["t"] for x in hd["lines"]),
            hadith_src,
        ),
    ]
    if bay:
        lines.append(row("bayan", f"**{bay.get('title', '')}**<br>" + "<br>".join(bay["lines"]), "بحار الأنوار ج٧ ص١٩٣ · تفسير كنز الدقائق ج١٤ ص٤١ · تأويل الآيات ج١ ص٧١٦"))
    if san:
        lines.append(
            row(
                "sanad",
                f"مُهر: **{san.get('verdict', '')}** — {san.get('verdict_sub', '')}<br>سطر کوچک: {san.get('note', '')}",
                "جمع‌بندیِ تحقیقِ سند در بطاقه‌های ۳ و ۴",
            )
        )
    lines.append(row("cta", f"**{c['cta'].get('line1', '')}**" + (f"<br>{c['cta']['line2']}" if c["cta"].get("line2") else "") + f"<br>منابع بالای قاب: {' • '.join(c.get('sources', []))}", "—"))
    lines += ["", "## رویدادهای صوتی (auto)", "", "```"]
    for x in p["sfx"]:
        lines.append(f"{x['at']:>5} f  ({sec(x['at'], fps):>5}s)  {x['src']:<10} vol {x['vol']}")
    lines += ["```", ""]
    if c.get("sources"):
        lines += ["## منابع روی قاب", ""] + [f"- {x}" for x in c["sources"]] + [""]
    lines += [
        "## مراجع کاملِ بطاقه‌ها (برای کپشن و کامنت سنجاق‌شده)",
        "",
        "- بطاقهٔ ۱: وسائل الشيعة ج٤ ص٥٧؛ صفات الشيعة ج١ ص٢؛ بحار الأنوار ج٦٥ ص١٦٧؛ بحار الأنوار ج٧٩ ص٢٩١",
        "- بطاقهٔ ۲: تأويل الآيات ج١ ص٧١٦؛ بحار الأنوار ج٧ ص١٩٣؛ تفسير كنز الدقائق ج١٤ ص٤١",
        "",
        "> نکتهٔ امانت‌داری: در بطاقهٔ ۳ زنجیره «عن علي بن سالم، عن أبيه» چاپ شده و در نتیجهٔ همان بطاقه و در",
        "> فهرست رجالِ بطاقهٔ ۴ نام‌های «علي بن أبي حمزة البطائني» و «سالم البطائني» آمده است. در این ریل نام",
        "> راویان روی قاب نیامده تا دو صورت با حدس یکی نشود؛ پیش از درجِ نام‌ها در کپشن/کامنت، باید صورت دقیق",
        "> زنجیره تأیید شود.",
        "",
    ]
    Path(a.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
