# 🐞 نقشه‌راه کامل باگ‌بانتی — از صفر تا حرفه‌ای

سایت زنده: **https://hack3rrabbit.github.io/bug-bounty-roadmap/**

یک نقشه‌راه **روز‌به‌روز، دقیق و ۱۰۰٪ رایگان** به زبان فارسی برای کسی که هیچ پیش‌زمینه‌ای در
امنیت ندارد و می‌خواهد به یک باگ‌بانتی‌هانتر حرفه‌ای تبدیل شود.

## این نقشه‌راه چیست؟

بر خلاف اکثر رودمپ‌های کلی («SQLi یاد بگیر»، «XSS یاد بگیر»)، این پروژه برنامه را به
**وظایف روزانهٔ مشخص** با **منبع رایگان دقیق** تقسیم کرده — هر روز می‌دانی امروز دقیقاً
باید چه کاری انجام بدهی و از کجا یاد بگیری.

نقشه‌راه بر پایهٔ تحقیق روی این منابع ساخته شده:

- محتوای رایگان **یاشار شاهین‌زاده** (بنیان‌گذار Voorivex): کانال یوتیوب، ویدیوی نقشه‌راه،
  وبلاگ [memoryleaks.ir](https://memoryleaks.ir/how-to-become-a-hacker/)، و دورهٔ رایگان
  «آموزش امنیت اپلیکیشن از صفر» در مکتب‌خونه
- بلاگ رسمی [Voorivex Team — Bug Bounty Roadmap from Scratch](https://blog.voorivex.team/bug-bounty-roadmap-from-scratch)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) — استاندارد صنعتی و کاملاً رایگان
- [Hacker101](https://www.hacker101.com/) (ساختهٔ HackerOne، شامل CTF رایگان)
- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)
- [NahamSec — Resources for Beginner Bug Bounty Hunters](https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters)
- Rana Khalil، Jason Haddix (Bug Hunter's Methodology)، TryHackMe، PentesterLab، Bugcrowd University،
  OWASP (Top 10, API Security Top 10, MASTG)، و ده‌ها منبع رایگان دیگر

## ساختار

نقشه‌راه به **۱۱ فاز** تقسیم شده، از مبانی لینوکس و شبکه تا شکار واقعی و گزارش‌نویسی حرفه‌ای:

| فاز | موضوع |
|---|---|
| ۰ | ذهنیت و راه‌اندازی محیط |
| ۱ | لینوکس و خط فرمان (OverTheWire Bandit) |
| ۲ | شبکه و پروتکل HTTP |
| ۳ | برنامه‌نویسی برای هکرها (پایتون، جاوااسکریپت، SQL) |
| ۴ | مبانی امنیت وب و Burp Suite |
| ۵ | هستهٔ آسیب‌پذیری‌های وب (PortSwigger Web Security Academy — تمام ۳۱ دستهٔ آسیب‌پذیری) |
| ۶ | تمرین متمرکز فارسی (Voorivex) و Hacker101 CTF |
| ۷ | Recon و متدولوژی حرفه‌ای شکار |
| ۸ | امنیت موبایل و API/GraphQL |
| ۹ | شکار واقعی، گزارش‌نویسی و پورتفولیو |
| ۱۰ | مباحث پیشرفته و رشد مستمر |

هر روز شامل: عنوان مشخص، توضیح دقیق کار، یک یا چند منبع رایگان با لینک مستقیم، و تخمین زمان است.
پیشرفت شما با تیک‌زدن هر روز در مرورگر خودتان (`localStorage`) ذخیره می‌شود.

## توسعه محلی

```bash
git clone https://github.com/hack3rrabbit/bug-bounty-roadmap.git
cd bug-bounty-roadmap
python3 -m http.server 8000
# باز کن: http://localhost:8000
```

برای بازتولید داده‌های نقشه‌راه از منبع پایتون:

```bash
python3 generate_roadmap.py   # خروجی: data/roadmap.json
```

## مشارکت

این پروژه متن‌باز و جامعه‌محور است. اگر منبع رایگان معتبری سراغ داری که جا افتاده،
یا خطایی در روزهای برنامه پیدا کردی، Issue یا Pull Request بزن.

## سلب مسئولیت

این یک پروژهٔ غیررسمی است و هیچ ارتباط رسمی با Voorivex، یاشار شاهین‌زاده، PortSwigger
یا HackerOne ندارد — صرفاً با هدف گردآوری بهترین منابع رایگان آموزشی برای جامعهٔ فارسی‌زبان
ساخته شده است. همیشه تست امنیتی را فقط در محدودهٔ مجاز (Scope) برنامه‌های باگ‌بانتی یا
محیط‌های آموزشی قانونی انجام دهید.

## لایسنس

MIT
