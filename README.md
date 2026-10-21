# maalsadiqeen

مخزن اسکیل **«ریل‌ساز مع الصادقین»** (`maalsadiqeen-reel`) — تبدیل ورق‌های برند صفحهٔ @maalsadiqeen به ریل
عمودی ۱۰۸۰×۱۹۲۰ و ۳۰–۶۰ ثانیه‌ای: خواندن ورق، بریف، نگارش فصیح، ساخت پروژه، تلاوت و طراحی صدا، گیت کیفیت،
رندر، کاور، بیت‌شیت فارسی و پست‌کیت. راهنمای کامل خودِ اسکیل: [`SKILL.md`](maalsadiqeen-reel-maker/maalsadiqeen-reel/SKILL.md)
· معرفی و نصب: [`maalsadiqeen-reel-maker/README.md`](maalsadiqeen-reel-maker/README.md) · گزارش بازبینی:
[`REVIEW-fa.md`](maalsadiqeen-reel-maker/REVIEW-fa.md).

## نصب‌شده در این محیط

نسخهٔ مادر (فقط این‌جا ویرایش کنید): `maalsadiqeen-reel-maker/maalsadiqeen-reel/` — نام فنی `maalsadiqeen-reel`، نسخهٔ 2.0.0،
۱۰۱ فایل (SKILL.md + ۱۳ مرجع + ۱۹ اسکریپت پایتون + ۲ شل + assets + evals).

همین نسخه، بایت‌به‌بایت، در سه مسیر استاندارد نصب شده است:

| مسیر | دامنه | برای |
|---|---|---|
| `.claude/skills/maalsadiqeen-reel/` | پروژه (همین مخزن) | Claude Code و هر ایجنتی که اسکیل‌های پروژه را می‌خواند |
| `~/.claude/skills/maalsadiqeen-reel/` | کاربر | Claude Code در هر پوشه‌ای |
| `~/.agents/skills/maalsadiqeen-reel/` | کاربر (مسیر مشترک) | Codex / Copilot / Gemini CLI و بقیه |

نصب/همگام‌سازی دوباره و بررسی سلامت:

```bash
bash install-skill.sh           # کپی از نسخهٔ مادر به هر سه مسیر + مقایسهٔ بایت‌به‌بایت
bash install-skill.sh --check   # فقط بررسی: هر سه نسخه با مادر یکسان‌اند؟
```

اگر نسخهٔ مادر را تغییر دادید، فقط `bash install-skill.sh` را دوباره اجرا کنید؛ نسخه‌های نصب‌شده بازنویسی می‌شوند.

## اسکیل‌های مکمل نصب‌شده

چهار اسکیل بیرونی برای ارتقای اسکیل اصلی انتخاب، در `vendor/skills/` نگه‌داری و در همان سه مسیر نصب
شده‌اند (منبع، کامیت، ستاره‌ها، لایسنس و گزینه‌های ردشده: [`vendor/skills/README.md`](vendor/skills/README.md)):

| اسکیل | حوزه | منبع | ★ | لایسنس |
|---|---|---|---|---|
| `skill-creator` | ساخت، اعتبارسنجی و ارزیابی اسکیل | `anthropics/skills` | ۱۸۲٬۵۳۹ | Apache-2.0 |
| `ig-reel` | ریل وایرال اینستاگرام (۲۶ فرمول هوک، بیت‌شیت) | `Jakeschincariol/instagram-agent-skill` | ۲٬۲۰۸ | MIT |
| `virat-design` | طراحی مینیمال حرفه‌ای برای پست/کاروسل/پوستر/کاور | `viratk-dev/virat-design` | ۶ | MIT |
| `instagram-growth` | الگوریتم و رشد اینستاگرام ۲۰۲۶ | `social-media-skills/skills` | ۱۷۷ | MIT |

**قاعدهٔ تقدم:** برای هر ریل «مع الصادقین»، `maalsadiqeen-reel` خط اصلی است؛ سه اسکیل دیگر مرجع و
ابزارند، نه pipeline جایگزین. `virat-design` پالت پیش‌فرض خود را ندارد (فقط کاغذ/سبز/طلایی برند)، و
`instagram-growth` ارجاع‌های WoopSocial را باید نادیده گرفت. برای هوک عربی از `hook_score_ar.py` استفاده
کنید، نه `hookscore.py` انگلیسی.

پروفایل صدای برند برای `ig-reel` در `integrations/ig-reel/voice.md` است و در
`~/.claude/instagram/voice.md` و `~/.agents/instagram/voice.md` نصب می‌شود (اگر از قبل وجود داشته باشد
بازنویسی نمی‌شود).

## شروع کار در گفتگو

ورق‌ها (تصویر) را پیوست کنید و بنویسید: «از این ورق‌ها یک ریل برای مع الصادقین بساز». ایجنٹ خودش
`SKILL.md` را می‌خواند و گردش‌کار ۰–۷ را اجرا می‌کند. اگر خواستهٔ خاصی دارید بگویید: «نسخهٔ B هوک»،
«برش ۴:۵»، «۳۵ ثانیه برای مناسبت»، «با گوینده»، «با Remotion».

دستور آغاز هر جلسه:

```bash
source .claude/skills/maalsadiqeen-reel/scripts/env.sh   # مسیرها + بررسی ابزارها
```

سپس `SKILL.md` → مرحلهٔ ۰ (ابزارها)، ۱ (خواندن ورق و بریف)، ۲ (هوک و spec)، ۳ (build)، ۴ (صدا)، ۵ (verify)،
۶ (رندر)، ۷ (کاور/بیت‌شیت/پست‌کیت). خروجی‌ها به‌صورت پیش‌فرض در `./reel-work` و `./reel-deliver` ساخته می‌شوند
(در `.gitignore` هستند).

## وضعیت ابزارها (بررسی‌شده در ۲۰۲۶-۱۰-۲۱، بدون اجرای رندر)

| ابزار | وضعیت |
|---|---|
| Python 3.11.2 | ✓ (همهٔ ۱۹ اسکریپت با `py_compile` سبز) |
| Node 22.22.3 · npm 10.9.8 | ✓ |
| `numpy` · `pillow` | ✗ → `pip install numpy pillow` |
| `ffmpeg` / `ffprobe` | ✗ → `sudo apt-get install -y ffmpeg` (یا `pip install imageio-ffmpeg`؛ ffprobe جدا لازم است) |
| `hyperframes@0.8.157` در `~/reel-sadiqeen` | ✗ → `mkdir -p ~/reel-sadiqeen && cd ~/reel-sadiqeen && npm init -y && npm install --no-audit --no-fund hyperframes@0.8.157 playwright@1.64.1 && npx hyperframes browser ensure` |

`scripts/env.sh` همین بررسی‌ها را هر جلسه انجام می‌دهد و دستور نصب هر چیز کم را چاپ می‌کند.

## نقشهٔ ارتقا

نقد و نقشهٔ کامل ارتقای اسکیل به نسخهٔ ۳.۰ (ورودی متن، سناریوهای چندگانه با گیت انتخاب، کیت انتشار IG/FB/X،
بانک کامنت و هم‌ترازی کامل با هویت برند) در
[`maalsadiqeen-reel-maker/UPGRADE-PLAN-fa.md`](maalsadiqeen-reel-maker/UPGRADE-PLAN-fa.md) است. هنوز چیزی از
اسکیل تغییر نکرده؛ این سند فقط پیشنهاد است.

## خطوط قرمز اسکیل

بدون گوینده (مگر به‌درخواست)، بدون منبع/درجهٔ ساختگی، متن آیه و حدیث عیناً از ورق با اعراب، حداکثر ۶۰ ثانیه،
`verify.py` پیش از رندر، و رنگ‌ها فقط کاغذ/سبز/طلایی — هرگز قرمز.
