# ریل‌ساز مع الصادقین — Maalsadiqeen Reel Maker

**پوشهٔ اصلی اسکیل نهایی.** یک اسکیل ایجنت (استاندارد `SKILL.md`) که ورق‌های برند صفحهٔ «مع الصادقين»
(@maalsadiqeen) را به ریل عمودی ۳۰–۶۰ ثانیه‌ای، باوقار و آمادهٔ انتشار تبدیل می‌کند — با تلاوت، طراحی صدا،
گیت کیفیت، رندر، کاور، بیت‌شیت فارسی و پست‌کیت.

| | |
|---|---|
| **عنوان** | ریل‌ساز مع الصادقین · Maalsadiqeen Reel Maker |
| **نام فنی اسکیل** (`name` در frontmatter، نام پوشهٔ قابل نصب) | `maalsadiqeen-reel` |
| **نسخه** | 2.0.1 — ادغامِ بازبینی‌شدهٔ دو اسکیل قبلی (`maalsadiqeen-1` + `maalsadiqeen-reel`)؛ ۲٫۰٫۱ اصلاحاتِ کشف‌شده در تولید نخستین ریل با موتور Remotion |
| **موتور پیش‌فرض / جایگزین** | HyperFrames 0.8 / Remotion 4 (داخل همین اسکیل) |
| **خروجی** | MP4 ۱۰۸۰×۱۹۲۰ (۳۰ fps، ≤ ۶۰ s) + کاور + نسخهٔ ۴:۵ + بیت‌شیت + پست‌کیت |

## ساختار این پوشه

```
maalsadiqeen-reel-maker/            ← پوشهٔ اصلی (شما اینجا هستید)
├── README.md                        ← همین راهنما
├── REVIEW-fa.md                     ← گزارش بازبینی دو اسکیل قبلی بر اساس ۷ اسکیل مرجع و تصمیم‌های ادغام
└── maalsadiqeen-reel/               ← خودِ اسکیل — این پوشه را نصب کنید
    ├── SKILL.md                     ← دستورالعمل ایجنت (یک درِ ورودی، گردش‌کار ۰–۷، جدول تصمیم)
    ├── references/                  ← برند، تحلیل محتوا، هوک‌های عربی، روایت، نگارش، بلوک‌ها، صدا، موشن، QC، انتشار، رفع اشکال، Remotion
    ├── scripts/                     ← ۱۹ اسکریپت پایتون + ۲ شل (Python ≥ 3.9)
    ├── assets/                      ← فونت‌ها، لوگو، افکت‌ها، GSAP، نمونه‌ها، قالب Remotion
    ├── evals/                       ← ۵ سناریوی آزمون + روبریک
    └── agents/openai.yaml · LICENSE
```

## نصب

```bash
# Claude Code (پروژه‌ای)            → .claude/skills/maalsadiqeen-reel/SKILL.md
mkdir -p .claude/skills && cp -r maalsadiqeen-reel-maker/maalsadiqeen-reel .claude/skills/

# Codex / Copilot / Gemini CLI و بقیه (مسیر مشترک)
mkdir -p ~/.agents/skills && cp -r maalsadiqeen-reel-maker/maalsadiqeen-reel ~/.agents/skills/

# یا مستقیم از گیت‌هاب
npx skills add sadegh2200/my --skill maalsadiqeen-reel
```

پیش‌نیازها را `scripts/env.sh` خودش بررسی می‌کند و دستور نصبِ هر چیزِ کم را چاپ می‌کند: Python ≥ 3.9 با
`numpy` و `pillow`، `ffmpeg/ffprobe`، Node ≥ 22 و `hyperframes@0.8.157` (+ Chrome Headless Shell با
`npx hyperframes browser ensure`). برای موتور جایگزین: `scripts/setup_studio.py` (Remotion 4).

## چطور صدا کنید

ورق‌ها را پیوست کنید و بنویسید: «از این ورق‌ها یک ریل برای مع الصادقین بساز». دستیار خودش اسکیل را فعال
می‌کند (کلیدواژه‌ها: ریل، reel، مع الصادقین، maalsadiqeen، ورق/پست، حدیث/آیه، اینستاگرام). اگر نوع خاصی
می‌خواهید بگویید: «نسخهٔ B هوک»، «برش ۴:۵»، «۳۵ ثانیه برای مناسبت»، «با گوینده» (فقط اگر واقعاً گوینده
بخواهید)، «با Remotion» (اگر موتور جایگزین را می‌خواهید).

## چه چیزی می‌گیرد، چه چیزی می‌دهد

- **ورودی:** یک یا چند ورقِ برند (تصویر) — با آیه یا بی‌آیه؛ حدیث، قول عالم، سؤال، مناسبت یا ردّ شبهه.
- **خروجی:** ریل عمودی ۱۰۸۰×۱۹۲۰ (۳۰ تا ۶۰ ثانیه، پیش‌فرض ۴۵)، کاور، بیت‌شیت فارسی، پست‌کیت (کپشن، کامنت
  سنجاق‌شدهٔ منابع، هوک‌های جایگزین، چک‌لیست انتشار)، و در صورت نیاز نسخهٔ ۴:۵ فید و هوک B.
- **سیاست صدا:** بدون گویندهٔ انسانی/مصنوعی (مگر خودتان بخواهید)؛ تلاوت قرآن وقتی آیه هست؛ طراحی صدا +
  بستر ملایم؛ مسترینگ −۱۵٫۵ LUFS. ویدیو باید بی‌صدا هم کامل فهمیده شود.

## مسیر کار (موتور پیش‌فرض)

| مرحله | ابزار | نتیجه |
|---|---|---|
| ۰ | `source scripts/env.sh` | مسیرها (`SKILL_DIR`, `REEL_WORK`, `REEL_DELIVER`, `HF_WORKDIR`) + بررسی ابزارها |
| ۱ | خواندن ورق‌ها + `references/content-analysis.md` | بریف: یک ایده، کلمهٔ مفصل، غافلگیری، حجّت، جملهٔ پایانی، دسته‌بندی A–F |
| ۲ | `hook_score_ar.py` + `new_spec.py` + `references/hooks-ar.md`, `narrative.md`, `arabic-copy.md` | سه هوک امتیازدهی‌شده؛ سناریوی فصیح به‌صورت spec (JSON) |
| ۳ | `build_reel.py` | پروژهٔ HyperFrames (HTML+GSAP) با فونت‌ها و تایپوگرافی اندازه‌شده |
| ۴ | `recite.py`، `cues.py`، `mix.py`، `gen_bed.py` | تلاوت هم‌زمان با کلمات، افکت‌ها، بستر، مسترینگ −۱۵٫۵ LUFS |
| ۵ | `verify.py` | گیت کیفیت: قواعد ریتم، `hyperframes check`، اسنپ‌شات‌های کلیدی (`qc/sheet.jpg`) — پیش از رندر |
| ۶ | `render.sh` + `verify.py --render` | رندر ۱۰۸۰×۱۹۲۰ و بررسی فنی خروجی |
| ۷ | `export_variants.py`، `beat_sheet.py`، `post_kit.py` + `references/publish.md` | کاور، ۴:۵، بیت‌شیت، پست‌کیت، توصیهٔ انتشار و سنجش A/B |

## الگوهای روایی (پیش‌فرض بر اساس محتوای ورق)

- **A** سؤال → جواب معصوم (آیه + حدیث + سند) — همان ساختار ریل «کونوا مع الصادقین».
- **B** یک کلمه معنا را عوض می‌کند (فقط حدیث). **C** تصحیح یک تصور (قول عالم/مفهوم).
- **D** سؤال → جواب (پرسش رایج). **E** مناسبت (ولادت/شهادت/عید). **F** ردّ شبهه (آرام و مستند).

## موتور جایگزین: Remotion studio

برای کاروسل‌های «حدیث + صفات شماره‌دار + سلسلهٔ سند» (مثل ریل «شیعتنا المسلّمون لأمرنا») قالب Remotion
صحنه‌های اختصاصی دارد: زنجیرهٔ راویان با مهر «ثقة»، مُهر نتیجه، چیپ‌های پیشرفت. دستورالعمل کامل در
`maalsadiqeen-reel/references/remotion-studio.md` و اسکیمای `content.json` در `remotion-schema.md`؛ قالب در
`assets/remotion-template/` و نمونه‌ها در `assets/examples/shiatuna/` و `variant-bayan/`.

## خطوط قرمز

۱) بدون گوینده مگر به درخواست شما. ۲) هیچ منبع یا درجهٔ سندی ساخته نمی‌شود؛ اگر روی ورق نیست، بلوک «سند» حذف
می‌شود و به شما گفته می‌شود. ۳) متن آیه/حدیث عیناً از ورق، با اعراب؛ کلمهٔ ناخوانا علامت‌گذاری می‌شود.
۴) حداکثر ۶۰ ثانیه. ۵) قبل از رندر، همیشه `verify.py` و دیدن فریم‌ها. ۶) رنگ قرمز هرگز؛ فقط کاغذ، سبز، طلایی.

## اجرای سریع نمونه‌ها

```bash
cd maalsadiqeen-reel-maker/maalsadiqeen-reel
source scripts/env.sh
python3 scripts/build_reel.py assets/examples/sadiqeen-9-119.silent.json --out "$REEL_WORK/demo"   # بازسازی ریل ۴۵ ثانیه‌ای
python3 scripts/mix.py "$REEL_WORK/demo" && python3 scripts/verify.py "$REEL_WORK/demo"
bash scripts/render.sh "$REEL_WORK/demo" "$REEL_DELIVER/demo.mp4"
```

نمونهٔ دوم: `assets/examples/hadith-only.json` → ریل ۴۱ ثانیه‌ای بدون آیه («النَّاسُ أَعْدَاءُ مَا جَهِلُوا»).

## چه چیزی آزمایش شده و چه چیزی باید در محیط شما یک‌بار اجرا شود

کل مسیر پایتونی هر دو موتور (build → mix → verify → بیت‌شیت/کاور/پست‌کیت؛ plan/validate/make_audio؛ `tsc` و
`remotion bundle` قالب؛ `hyperframes lint`) آزمایش شده است — جزئیات در `REVIEW-fa.md`. آنچه نیاز به مرورگر
یا اینترنت دارد (`hyperframes check/snapshot/render`، `remotion render`، دانلود تلاوت) باید یک‌بار در محیط
خودتان اجرا شود؛ `env.sh` می‌گوید چه چیزی کم است.
