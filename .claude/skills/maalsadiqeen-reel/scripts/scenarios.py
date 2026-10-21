#!/usr/bin/env python3
"""
scenarios.py — the gate between thinking and building.

    scenarios.py init    <slug> [--brief brief.json] [--count 4] [--out scenarios.json]
    scenarios.py validate <slug|scenarios.json> [--brief …]
    scenarios.py score    <slug|scenarios.json> [--brief …] [--log config/content-log.json] [--json]
    scenarios.py render   <slug|scenarios.json> [--brief …] [--preview preview/] [--no-preview]
    scenarios.py select   <slug|scenarios.json> --choose 2,4 [--out selected.json]
    scenarios.py variant  <slug|scenarios.json> --id 2 --hook "…" [--out variant-2.json]
    scenarios.py compile  <slug|scenarios.json> --id 2 --out spec.json [--brand config/brand.json]

A scenario is a complete, buildable plan (see references/scenarios.md). This script validates it,
scores it, renders `scenarios.md` + preview frames, and compiles the chosen one into a spec that
`build_reel.py` understands. It never invents copy: the agent writes the scenarios, the script
enforces the rules.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))

from _common import strip_tashkeel, words  # noqa: E402
import hook_score_ar  # noqa: E402
import preview_frames  # noqa: E402

BRAND_PATH = SKILL / "config" / "brand.json"
LOG_PATH = SKILL / "config" / "content-log.json"
BLOCK_TYPES = {"hook", "verse", "contrast", "answer", "proof", "cta", "quote", "list", "title"}
SACRED_FIELDS = {"verse": ["label", "lines"], "quote": ["text"], "answer": ["hero"], "hook": ["lead"]}


def load_json(p: Path, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return default


def brand_cfg(path: str | None = None) -> dict:
    return load_json(Path(path) if path else BRAND_PATH, {}) or {}


def resolve(spec_or_slug: str) -> Path:
    p = Path(spec_or_slug)
    if p.suffix == ".json" and p.exists():
        return p
    work = Path(os.environ.get("REEL_WORK", "reel-work")) / spec_or_slug
    for name in ("scenarios.json", "scenes.json"):
        if (work / name).exists():
            return work / name
    sys.exit(f"scenarios file not found for «{spec_or_slug}» (looked in {work})")


def workdir_for(path: Path) -> Path:
    return path.parent


def brief_for(path: Path, explicit: str | None) -> dict:
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = workdir_for(path) / p
        return load_json(p, {}) or {}
    for name in ("brief.json", "brief.seed.json"):
        p = workdir_for(path) / name
        if p.exists():
            return load_json(p, {}) or {}
    return {}


# ----------------------------------------------------------------------------- validate
def validate(doc: dict, brand: dict) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    scs = doc.get("scenarios") or []
    if len(scs) < 3:
        errs.append(f"only {len(scs)} scenarios — the gate needs at least 3 (aim 4)")
    ids, angles, titles = set(), {}, {}
    dur_min, dur_max = (brand.get("defaults", {}).get("duration_window") or [30, 50])
    for sc in scs:
        sid = sc.get("id")
        label = f"#{sid}"
        if sid in ids:
            errs.append(f"{label}: duplicate id")
        ids.add(sid)
        if not sc.get("title_fa"):
            errs.append(f"{label}: title_fa missing")
        angle = sc.get("angle", "")
        angles[angle] = angles.get(angle, 0) + 1
        titles[sc.get("title_fa", "")] = titles.get(sc.get("title_fa", ""), 0) + 1
        if sc.get("archetype") not in "ABCDEF":
            warns.append(f"{label}: archetype «{sc.get('archetype')}» not in A–F")
        if not sc.get("one_sentence"):
            errs.append(f"{label}: one_sentence missing (the 14-word test)")
        elif words(sc["one_sentence"]) > 14:
            warns.append(f"{label}: one_sentence is {words(sc['one_sentence'])} words — tighten to ≤ 14")
        hook = sc.get("hook") or {}
        htext = (hook.get("text") or "").strip()
        if not htext:
            errs.append(f"{label}: hook.text missing")
        else:
            n = words(htext)
            if n < 3 or n > 9:
                warns.append(f"{label}: hook is {n} words (aim 4–8)")
            for bad in brand.get("forbidden_on_screen", []):
                if bad in htext:
                    errs.append(f"{label}: forbidden wording in hook — «{bad}»")
        life = (sc.get("life_impact") or "").strip()
        if not life or life == "…":
            errs.append(f"{label}: life_impact missing — one concrete change in the viewer's week")
        elif words(life) > 32:
            warns.append(f"{label}: life_impact is {words(life)} words — one sentence")
        scenes = sc.get("scenes") or []
        if not scenes:
            errs.append(f"{label}: no scenes")
            continue
        if scenes[0].get("type") != "hook":
            errs.append(f"{label}: first scene must be hook")
        if scenes[-1].get("type") != "cta":
            warns.append(f"{label}: last scene is not cta (no brand card)")
        total = 0.0
        for i, s in enumerate(scenes, 1):
            t = s.get("type")
            if t not in BLOCK_TYPES:
                errs.append(f"{label} s{i}: unknown block type «{t}»")
            sec = s.get("seconds")
            if not isinstance(sec, (int, float)) or sec <= 0:
                errs.append(f"{label} s{i}: seconds must be a positive number")
            else:
                total += float(sec)
            if t == "verse":
                lines = s.get("lines") or []
                if not lines or not all(isinstance(x, list) and x for x in lines):
                    errs.append(f"{label} s{i}: verse.lines must be a list of word-lists")
                hi = (s.get("highlight") or {}).get("words") or []
                flat = [w for ln in lines for w in ln] if lines else []
                if hi and flat and max(hi) > len(flat):
                    warns.append(f"{label} s{i}: highlight words {hi} exceed {len(flat)} words")
            if t == "cta" and not (s.get("brand") or {}).get("handle"):
                warns.append(f"{label} s{i}: cta brand card without a handle")
            if t == "proof":
                for c in s.get("cards") or []:
                    if not c.get("book"):
                        warns.append(f"{label} s{i}: proof card without a book")
                    if not c.get("grade") and s.get("seal"):
                        errs.append(f"{label} s{i}: seal «صحیح السند» with no stated grading — invented authority")
                    loc = c.get("loc") or ""
                    if re.search(r"[0-9]", loc):
                        warns.append(f"{label} s{i}: use Arabic-Indic digits in loc «{loc}»")
            if t in SACRED_FIELDS:
                text = json.dumps(s.get("lines", "") if t == "verse" else s.get("text", ""), ensure_ascii=False)
                text += " " + str(s.get("label", "")) + " " + str(s.get("hero", "")) + " " + str(s.get("lead", ""))
                if len(text) > 30 and not re.search(r"[\u064B-\u0652]", text):
                    warns.append(f"{label} s{i}: {t} has no tashkeel — sacred text needs vocalisation")
        if total and not (30 <= total <= 60):
            errs.append(f"{label}: total {total:.1f}s — must be 30–60 s")
        elif total and not (dur_min <= total <= dur_max):
            warns.append(f"{label}: total {total:.1f}s outside the preferred {dur_min}–{dur_max} s window")
        needs = sc.get("needs") or {}
        if s_has_proof(scenes) and not needs.get("proof"):
            warns.append(f"{label}: has a proof block but needs.proof is empty — where does it come from?")
        if not needs.get("recitation") and any(s.get("type") == "verse" for s in scenes):
            warns.append(f"{label}: verse on screen without needs.recitation (recitation is the brand default for āyāt)")
    for a, n in angles.items():
        if a and n > 1:
            warns.append(f"angle «{a}» is used by {n} scenarios — the choice collapses into an A/B variant")
    return errs, warns


def s_has_proof(scenes: list[dict]) -> bool:
    return any(s.get("type") == "proof" for s in scenes)


# ----------------------------------------------------------------------------- score
def score_all(doc: dict, brief: dict, brand: dict, log: dict | None) -> list[dict]:
    log = log or {}
    recent = (log.get("reels") or [])[-10:]
    last3 = recent[-3:]
    last2 = recent[-2:]
    last5 = recent[-5:]
    out = []
    for sc in doc.get("scenarios") or []:
        h = hook_score_ar.score(((sc.get("hook") or {}).get("text") or ""))
        sc["hook"]["score"] = h["score"]
        sc["hook"]["grade"] = h["grade"]
        sc["hook"]["dimensions"] = h.get("dimensions", {})

        needs = sc.get("needs") or {}
        cards = [c for s in sc.get("scenes") or [] if s.get("type") == "proof" for c in (s.get("cards") or [])]
        if any(c.get("grade") for c in cards):
            evidence = 20
        elif cards or needs.get("proof"):
            evidence = 14
        else:
            evidence = 4

        scenes = sc.get("scenes") or []
        clarity = 0
        clarity += 6 if sc.get("one_sentence") and words(sc["one_sentence"]) <= 14 else 2
        clarity += 4 if scenes and all(s.get("type") in BLOCK_TYPES for s in scenes) else 1
        clarity += 3 if scenes and scenes[0].get("type") == "hook" and scenes[-1].get("type") == "cta" else 0
        secs = [float(s.get("seconds", 0)) for s in scenes]
        clarity += 2 if secs and max(secs) <= 12 and min(secs) >= 2.5 else 1
        clarity = min(15, clarity)

        freshness = 15
        if sc.get("angle") and any(r.get("angle") == sc.get("angle") for r in last2):
            freshness -= 6
        if sc.get("archetype") and any(r.get("archetype") == sc.get("archetype") for r in last3):
            freshness -= 4
        if sc.get("hook", {}).get("formula") and any(r.get("hook_formula") == sc["hook"]["formula"] for r in last5):
            freshness -= 5
        freshness = max(3, freshness)

        cost = {"S": 10, "M": 7, "L": 3}.get(str(sc.get("cost", "M")).upper(), 7)

        total = round(0.40 * h["score"] + evidence + clarity + freshness + cost)
        sc["scores"] = {"hook": h["score"], "evidence": evidence, "clarity": clarity,
                        "freshness": freshness, "cost": cost, "total": total}
        sc["total_score"] = total
        out.append(sc)
    doc["scenarios"] = sorted(out, key=lambda s: -s.get("total_score", 0))
    for i, sc in enumerate(doc["scenarios"], 1):
        sc["rank"] = i
    return doc["scenarios"]


def diversity_warnings(doc: dict, log: dict | None) -> list[str]:
    log = log or {}
    recent = (log.get("reels") or [])[-10:]
    warns = []
    for sc in doc.get("scenarios") or []:
        if any(r.get("angle") == sc.get("angle") for r in recent[-2:]):
            warns.append(f"#{sc.get('id')}: زاویهٔ «{sc.get('angle')}» در دو ریل اخیر استفاده شده")
        if any(r.get("archetype") == sc.get("archetype") for r in recent[-3:]):
            warns.append(f"#{sc.get('id')}: الگوی «{sc.get('archetype')}» در سه ریل اخیر تکرار شده")
        if any(r.get("hook_formula") == (sc.get("hook") or {}).get("formula") for r in recent[-5:]):
            warns.append(f"#{sc.get('id')}: فرمول هوک {sc['hook'].get('formula')} در پنج ریل اخیر آمده")
    return warns


# ----------------------------------------------------------------------------- markdown
def render_md(doc: dict, brief: dict, out: Path, diversity: list[str]) -> None:
    scs = doc.get("scenarios") or []
    lines = [
        f"# چهار سناریو — {doc.get('slug', '')}", "",
        f"**ایدهٔ واحد بریف:** {brief.get('one_idea') or brief.get('classification', {}).get('archetype', '—')}",
        f"**شکل پیشنهادی:** {brief.get('shape', {}).get('reason', '—')}", "",
        "| # | امتیاز | زاویه | الگو | مدت | هزینه | ریسک | عنوان |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for sc in scs:
        dur = sum(float(s.get("seconds", 0)) for s in sc.get("scenes") or [])
        lines.append(f"| {sc.get('id')} | {sc.get('total_score')}/100 | {sc.get('angle')} | {sc.get('archetype')} "
                     f"| {dur:.1f}s | {sc.get('cost')} | {sc.get('risk')} | {sc.get('title_fa')} |")
    if diversity:
        lines += ["", "> **هشدار تنوع:** " + "؛ ".join(diversity)]
    for sc in scs:
        s = sc.get("scores") or {}
        h = sc.get("hook") or {}
        lines += ["", "---", "", f"## سناریو {sc.get('id')} — {sc.get('title_fa')}", "",
                  f"**زاویه:** {sc.get('angle')} · **الگو:** {sc.get('archetype')} · "
                  f"**امتیاز:** {sc.get('total_score')}/100 (هوک {s.get('hook')} · سند {s.get('evidence')} · "
                  f"شفافیت {s.get('clarity')} · تازگی {s.get('freshness')} · هزینه {s.get('cost')})",
                  "", f"**ایده در یک جمله:** {sc.get('one_sentence')}", "",
                  f"**هوک:** «{h.get('text', '')}» — نمرهٔ {h.get('score')} ({h.get('grade')})"
                  + (f" · فرمول {h.get('formula')}" if h.get("formula") else ""), "",
                  "**صحنه‌ها:**", "", "| زمان | بلوک | روی صفحه |", "|---|---|---|"]
        t = 0.0
        for scn in sc.get("scenes") or []:
            d = float(scn.get("seconds", 0))
            content = scene_summary(scn)
            lines.append(f"| {t:.1f}–{t + d:.1f}s | {scn.get('type')} | {content} |")
            t += d
        needs = sc.get("needs") or {}
        lines += ["", f"**نیازها:** تلاوت: {needs.get('recitation') or '—'} · منابع: "
                      + ("؛ ".join(needs.get("proof") or []) or "—"),
                  f"**ریسک:** {sc.get('risk')} · **هزینه:** {sc.get('cost')}",
                  "", f"**چرا این سناریو:** {sc.get('why_fa', '—')}"]
    lines += ["", "---", "",
              "## انتخاب", "",
              "کدام را بسازم؟ مثلاً «۲» یا «۲ و ۴». تا پاسخ شما هیچ ساخت‌ی آغاز نمی‌شود.", ""]
    out.write_text("\n".join(lines), encoding="utf-8")


def scene_summary(scn: dict) -> str:
    t = scn.get("type")
    if t == "hook":
        return " · ".join(x for x in (scn.get("lead", ""), scn.get("line1", ""), scn.get("line2", ""), scn.get("sub", "")) if x)
    if t == "verse":
        return " ".join(w for line in scn.get("lines") or [] for w in line)
    if t == "contrast":
        return f"{scn.get('wrong_label', '')} {scn.get('wrong', '')} / {scn.get('right_label', '')} {scn.get('right', '')}"
    if t == "answer":
        return f"{scn.get('q1', '')} — {scn.get('hero', '')}"
    if t == "proof":
        return "؛ ".join(f"{c.get('book', '')} {c.get('loc', '')} {c.get('grade', '')}".strip() for c in scn.get("cards") or [])
    if t == "cta":
        return f"{scn.get('line1', '')} {scn.get('line2', '')} — {scn.get('share', '')}"
    if t == "quote":
        text = scn.get("text")
        return " ".join(text) if isinstance(text, list) else str(text or "")
    if t == "list":
        return f"{scn.get('title', '')}: " + " · ".join(scn.get("items") or [])
    if t == "title":
        return f"{scn.get('kicker', '')} — {scn.get('title', '')}"
    return ""


# ----------------------------------------------------------------------------- compile
def compile_spec(sc: dict, brand: dict, spec_id: str) -> dict:
    scenes, t = [], 0.0
    for i, src in enumerate(sc.get("scenes") or []):
        d = {k: v for k, v in src.items() if k not in ("seconds",)}
        d["id"] = f"s{i + 1}"
        d["start"] = round(t, 2)
        t = round(t + float(src.get("seconds", 0)), 2)
        d["end"] = t
        scenes.append(d)
    audio = {"mode": "silent", "file": "mix.wav", "bed": {"gain_db": -7}, "auto_sfx": True,
             "target_lufs": (brand.get("defaults", {}) or {}).get("lufs", -15.5)}
    rec = (sc.get("needs") or {}).get("recitation")
    if rec:
        audio["recitation"] = {"ref": rec,
                               "edition": (brand.get("defaults", {}) or {}).get("recitation_edition", "ar.mahermuaiqly")}
    return {
        "id": spec_id,
        "title": sc.get("one_sentence") or sc.get("title_fa") or spec_id,
        "scenario": {"id": sc.get("id"), "title_fa": sc.get("title_fa"), "angle": sc.get("angle"),
                     "archetype": sc.get("archetype"), "hook": sc.get("hook"), "score": sc.get("total_score")},
        "duration": round(t, 2),
        "life_impact": sc.get("life_impact") or "",
        "brand": {"handle": brand.get("handle", "maalsadiqeen")},
        "audio": audio,
        "scenes": scenes,
    }


# ----------------------------------------------------------------------------- init
TEMPLate_ANGLES = [
    ("سؤال محوري", "A", "M"),
    ("تصحيح سوء فهم", "C", "M"),
    ("كلمة واحدة", "B", "S"),
    ("تطبيق معاصر", "D", "S"),
    ("سلسلة السند", "A", "L"),
    ("سيرة / لحظة", "E", "S"),
    ("سياق النصّ", "A", "M"),
    ("ردّ شبهة بهدوء", "F", "L"),
]


def init(slug: str, brief: dict, count: int, brand: dict, out: Path) -> dict:
    quotes = brief.get("quotes") or []
    primary = quotes[0] if quotes else {}
    rec = ""
    for q in quotes:
        if q.get("kind") == "quran":
            m = re.search(r"([٠-٩0-9]+)\s*[:：]\s*([٠-٩0-9]+)", q.get("source", {}).get("loc", ""))
            if m:
                rec = f"{m.group(1)}:{m.group(2)}"
                break
    scenarios = []
    for i, (angle, arch, cost) in enumerate(TEMPLate_ANGLES[:count], 1):
        scenarios.append({
            "id": i,
            "title_fa": f"… ({angle})",
            "angle": angle,
            "archetype": arch,
            "one_sentence": "…",
            "hook": {"text": "…", "formula": 0},
            "scenes": [
                {"type": "hook", "seconds": 3.4, "lead": "«…»", "line1": "…", "line2": "…؟", "sub": "…"},
                {"type": "quote", "seconds": 9.0, "label": "قَالَ … عَلَيْهِ السَّلام",
                 "text": primary.get("text", "…")[:120] or "…", "reveal": "words",
                 "attribution": "— … ج… ص…"},
                {"type": "contrast", "seconds": 8.0, "wrong_label": "الظَّنُّ:", "wrong": "…",
                 "right_label": "وَالنَّصُّ:", "right": "…", "line3": "…"},
                {"type": "proof", "seconds": 8.0,
                 "cards": [{"book": (primary.get("source", {}) or {}).get("book", "…"),
                            "loc": (primary.get("source", {}) or {}).get("loc", "ج… ص…"),
                            "grade": (primary.get("source", {}) or {}).get("grade", "")}],
                 "line1": "…"},
                {"type": "cta", "seconds": 6.4, "line1": "…", "line2": "…", "share": "أَرْسِلْهَا لِمَنْ تُحِبّ",
                 "final": "…", "brand": {"handle": brand.get("handle", "maalsadiqeen")}},
            ],
            "needs": {"recitation": rec, "proof": [x for x in [primary.get("source", {}).get("book")] if x], "assets": []},
            "life_impact": "…",
            "risk": "low",
            "cost": cost,
            "why_fa": "…",
        })
    doc = {"schema": 3, "slug": slug, "brief": brief.get("slug", slug) + ".json",
           "defaults": {"duration": 40, "archetype": scenarios[0]["archetype"], "language": "ar"},
           "scenarios": scenarios}
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return doc


# ----------------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("target", help="slug or scenarios.json")
        p.add_argument("--brief", default=None)
        p.add_argument("--brand", default=None)
        p.add_argument("--log", default=None)

    p = sub.add_parser("init")
    p.add_argument("slug")
    p.add_argument("--brief", default=None)
    p.add_argument("--count", type=int, default=4)
    p.add_argument("--out", default=None)
    p.add_argument("--brand", default=None)

    for name in ("validate", "score", "render", "select", "variant", "compile"):
        common(sub.add_parser(name))

    sp = sub.choices["render"]
    sp.add_argument("--preview", default="preview")
    sp.add_argument("--no-preview", action="store_true")
    sp.add_argument("--out", default=None)
    sub.choices["score"].add_argument("--json", action="store_true")
    sub.choices["select"].add_argument("--choose", required=True, help="e.g. 2,4 or 2")
    sub.choices["select"].add_argument("--out", default=None)
    sub.choices["variant"].add_argument("--id", type=int, required=True)
    sub.choices["variant"].add_argument("--hook", required=True)
    sub.choices["variant"].add_argument("--out", default=None)
    sub.choices["compile"].add_argument("--id", type=int, required=True)
    sub.choices["compile"].add_argument("--out", required=True)

    a = ap.parse_args()
    brand = brand_cfg(a.brand)

    if a.cmd == "init":
        work = Path(os.environ.get("REEL_WORK", "reel-work")) / a.slug
        work.mkdir(parents=True, exist_ok=True)
        brief_path = Path(a.brief) if a.brief else work / "brief.seed.json"
        brief = load_json(brief_path, {}) or {}
        out = Path(a.out) if a.out else work / "scenarios.json"
        doc = init(a.slug, brief, a.count, brand, out)
        print(f"wrote {out} — {len(doc['scenarios'])} scenarios, every «…» must be replaced")
        return

    path = resolve(a.target)
    doc = load_json(path, {}) or {}
    brief = brief_for(path, a.brief)
    log = load_json(Path(a.log) if a.log else LOG_PATH, {}) or {}

    if a.cmd == "validate":
        errs, warns = validate(doc, brand)
        for w in warns:
            print("  ⚠", w)
        for e in errs:
            print("  ✗", e)
        print(f"{len(errs)} errors · {len(warns)} warnings")
        sys.exit(1 if errs else 0)

    if a.cmd == "score":
        score_all(doc, brief, brand, log)
        div = diversity_warnings(doc, log)
        if a.json:
            print(json.dumps({"scenarios": doc["scenarios"], "diversity": div}, ensure_ascii=False, indent=2))
        else:
            for sc in doc["scenarios"]:
                print(f"#{sc['id']} {sc['total_score']:3d}/100  {sc['angle']:<18} {sc['title_fa']}  (hook {sc['hook']['score']})")
            for w in div:
                print("  ⚠", w)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return

    if a.cmd == "render":
        errs, warns = validate(doc, brand)
        if errs:
            for e in errs:
                print("  ✗", e)
            sys.exit("fix the errors before rendering the scenarios")
        score_all(doc, brief, brand, log)
        div = diversity_warnings(doc, log)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        md = Path(a.out) if a.out else workdir_for(path) / "scenarios.md"
        render_md(doc, brief, md, div)
        print(f"wrote {md}")
        if not a.no_preview:
            preview_dir = workdir_for(path) / a.preview
            n = preview_frames.write_jpgs(doc["scenarios"], preview_dir, brand)
            if n:
                print(f"wrote {n} preview JPEGs → {preview_dir}")
            html_path = workdir_for(path) / "preview.html"
            preview_frames.write_html(doc["scenarios"], html_path, brand,
                                      title=f"مع الصادقين — {doc.get('slug', '')}")
            print(f"wrote {html_path}")
        for w in warns + div:
            print("  ⚠", w)
        print("\n⛔ GATE: wait for the user's choice before building (reel.py build --choose …).")
        return

    if a.cmd == "select":
        chosen = [int(x.strip()) for x in a.choose.replace("و", ",").split(",") if x.strip().isdigit()]
        scs = {s["id"]: s for s in doc.get("scenarios") or []}
        missing = [c for c in chosen if c not in scs]
        if missing:
            sys.exit(f"unknown scenario id(s): {missing}")
        out = Path(a.out) if a.out else workdir_for(path) / "selected.json"
        sel = {"slug": doc.get("slug"), "chosen": chosen,
               "scenarios": [scs[c] for c in chosen]}
        out.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"selected {chosen} → {out}")
        return

    if a.cmd == "variant":
        sc = next((s for s in doc.get("scenarios") or [] if s.get("id") == a.id), None)
        if not sc:
            sys.exit(f"scenario #{a.id} not found")
        h = hook_score_ar.score(a.hook)
        var = json.loads(json.dumps(sc))
        var["id"] = f"{a.id}b"
        var["title_fa"] = sc.get("title_fa", "") + " (هوک B)"
        var["hook"] = {"text": a.hook, "formula": (sc.get("hook") or {}).get("formula", 0),
                       "score": h["score"], "grade": h["grade"]}
        for s in var.get("scenes") or []:
            if s.get("type") == "hook":
                parts = a.hook.split("…")
                s["line1"] = parts[0].strip()[:24] or a.hook[:24]
                s["line2"] = (parts[1].strip() if len(parts) > 1 else "")[:20]
                break
        out = Path(a.out) if a.out else workdir_for(path) / f"variant-{a.id}.json"
        out.write_text(json.dumps({"slug": doc.get("slug"), "scenarios": [var]}, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        print(f"wrote {out} — hook scored {h['score']} ({h['grade']}); same scenes, same length")
        return

    if a.cmd == "compile":
        sc = next((s for s in doc.get("scenarios") or [] if s.get("id") == a.id), None)
        if not sc:
            sys.exit(f"scenario #{a.id} not found")
        spec = compile_spec(sc, brand, spec_id=f"{doc.get('slug', 'reel')}-{a.id}")
        Path(a.out).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {a.out} — {len(spec['scenes'])} scenes, {spec['duration']}s")
        return


if __name__ == "__main__":
    main()
