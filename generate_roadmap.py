#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولد داده‌های نقشه‌راه باگ‌بانتی (روز به روز)
خروجی: data/roadmap.json
"""
import json, os

# ---------------------------------------------------------------------------
# ساختار: هر فاز شامل عنوان، توضیح کوتاه، رنگ و لیستی از روزهاست.
# هر روز: عنوان کوتاه، هدف/تسک مشخص، منبع (نام + لینک)، و تخمین زمان (دقیقه)
# می‌تواند بیش از یک منبع داشته باشد -> resources: [{t: title, u: url}]
# ---------------------------------------------------------------------------

phases = []
day_counter = 0

def phase(pid, title, subtitle, icon, color):
    p = {"id": pid, "title": title, "subtitle": subtitle, "icon": icon, "color": color, "days": []}
    phases.append(p)
    return p

def d(p, title, task, resources, hours=2, kind="learn"):
    """kind: learn | practice | review | milestone"""
    global day_counter
    day_counter += 1
    p["days"].append({
        "day": day_counter,
        "title": title,
        "task": task,
        "resources": resources,
        "hours": hours,
        "kind": kind,
    })

def R(t, u):
    return {"t": t, "u": u}

# ===========================================================================
# فاز ۰ — شروع، ذهنیت و راه‌اندازی محیط
# ===========================================================================
p0 = phase("p0", "شروع؛ ذهنیت و راه‌اندازی محیط", "قبل از هر خط دستور، باید بدانی چرا و با چه ابزاری شروع می‌کنی", "🚀", "#7c3aed")

d(p0, "چرا باگ‌بانتی؟ و مسیر واقعی این حرفه",
  "مقالهٔ «چگونه هکر شویم» یاشار شاهین‌زاده را کامل بخوان. یک سند در Notion/Obsidian بساز و بخش «چرا این مسیر رو رفتم» را برای خودت با انگیزهٔ واقعی‌ات بنویس؛ این سند را در تمام مسیر آپدیت کن.",
  [R("وبلاگ یاشار شاهین‌زاده — چگونه هکر شویم", "https://memoryleaks.ir/how-to-become-a-hacker/"),
   R("نقشه‌راه باگ‌بانتی تیم Voorivex", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")],
  hours=2, kind="learn")

d(p0, "دیدن ویدیوی نقشه‌راه یاشار شاهین‌زاده",
  "کل ویدیوی نقشه‌راه را با یادداشت‌برداری ببین. هر توصیه‌ای که می‌دهد را در سند خودت به‌صورت چک‌لیست وارد کن — این چک‌لیست کنار این نقشه‌راه، راهنمای شخصی تو خواهد بود.",
  [R("ویدیوی نقشه‌راه — یاشار شاهین‌زاده (یوتیوب Voorivex)", "https://www.youtube.com/watch?v=_UxO2qKvCEQ"),
   R("کانال یوتیوب Voorivex", "https://www.youtube.com/@Voorivex")],
  hours=1, kind="learn")

d(p0, "ماشین مجازی لینوکس و راه‌اندازی محیط هک",
  "روی سیستم خودت VirtualBox/VMware نصب کن و توزیع Kali Linux یا Parrot OS را روی یک ماشین مجازی بالا بیاور. اسنپ‌شات اولیه بگیر تا هر وقت محیط خراب شد برگردی.",
  [R("دانلود Kali Linux", "https://www.kali.org/get-kali/"),
   R("VirtualBox (رایگان)", "https://www.virtualbox.org/"),
   R("راهنمای نصب Kali در VirtualBox", "https://www.kali.org/docs/virtualization/install-virtualbox-guest-vm/")],
  hours=2, kind="practice")

d(p0, "ساخت پروفایل و آشنایی با پلتفرم‌های باگ‌بانتی",
  "در HackerOne و Bugcrowd ثبت‌نام کن، بخش Hacktivity هر دو را مرور کن تا با فرمت گزارش‌های عمومی و نوع باگ‌های پذیرفته‌شده آشنا شوی. حداقل ۵ گزارش افشا‌شدهٔ واقعی را کامل بخوان.",
  [R("HackerOne Hacktivity", "https://hackerone.com/hacktivity"),
   R("Bugcrowd Crowdstream", "https://bugcrowd.com/crowdstream"),
   R("مخزن گزارش‌های افشاشدهٔ برتر (Awesome Bugbounty Writeups)", "https://github.com/devanshbatham/Awesome-Bugbounty-Writeups")],
  hours=2, kind="practice")

d(p0, "ابزار مستندسازی و متدولوژی شخصی",
  "یک Vault در Obsidian (یا Notion) بساز با پوشه‌های: Methodology، CVE/Writeups، Targets، Reports. از همین امروز هر نکته‌ای که یاد می‌گیری را همان‌جا یادداشت کن — این عادت مهم‌ترین ابزار یک هانتر حرفه‌ای است.",
  [R("Obsidian (رایگان)", "https://obsidian.md/"),
   R("راهنمای ساخت متدولوژی شخصی — Bug Bounty Roadmap (Voorivex)", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")],
  hours=1, kind="learn")

# ===========================================================================
# فاز ۱ — لینوکس و خط فرمان
# ===========================================================================
p1 = phase("p1", "لینوکس و خط فرمان", "بدون تسلط روی ترمینال، هیچ ابزار هک را نمی‌توانی درست اجرا کنی", "🐧", "#059669")

d(p1, "مبانی لینوکس: فایل‌سیستم و دستورات پایه",
  "فصل «Linux Basics» را تمرین کن: ls, cd, pwd, cat, cp, mv, rm, mkdir, man. برای هر دستور از man یا --help استفاده کن، نه گوگل.",
  [R("Linux Journey — بخش Grasshopper", "https://linuxjourney.com/lesson/the-shell"),
   R("TryHackMe — Linux Fundamentals Part 1 (رایگان)", "https://tryhackme.com/room/linuxfundamentalspart1")],
  hours=2, kind="learn")

d(p1, "OverTheWire Bandit — سطح ۰ تا ۲",
  "وارد سرور Bandit با SSH شو (level0/level0, پسورد: bandit0) و سه سطح اول را حل کن. یاد می‌گیری چطور به فایل‌های مخفی، فایل‌هایی با اسم عجیب و خروجی دستورات دسترسی پیدا کنی.",
  [R("OverTheWire Bandit", "https://overthewire.org/wargames/bandit/"),
   R("Bandit Level 0", "https://overthewire.org/wargames/bandit/bandit0.html")],
  hours=2, kind="practice")

d(p1, "Bandit — سطح ۳ تا ۶",
  "کار با فایل‌های مخفی، جست‌وجوی رکورسیو با find، و فیلتر کردن بر اساس نوع/حجم/مجوز فایل. از find و grep به‌صورت ترکیبی استفاده کن.",
  [R("Bandit Level 3", "https://overthewire.org/wargames/bandit/bandit3.html")],
  hours=2, kind="practice")

d(p1, "Bandit — سطح ۷ تا ۱۰",
  "grep پیشرفته، پردازش فایل‌های فشرده (tar/gzip/bzip2) و Base64/فایل باینری را تمرین کن.",
  [R("Bandit Level 7", "https://overthewire.org/wargames/bandit/bandit7.html")],
  hours=2, kind="practice")

d(p1, "متغیرها، پرمیشن‌ها و مالکیت فایل",
  "مفهوم rwx، chmod عددی/نمادین، chown، و متغیرهای محیطی (PATH, env) را یاد بگیر، سپس سطح‌های ۱۱ تا ۱۴ Bandit را حل کن.",
  [R("Bandit Level 11", "https://overthewire.org/wargames/bandit/bandit11.html")],
  hours=2, kind="practice")

d(p1, "SSH کلیدها، پورت‌ها و پروسه‌ها",
  "تولید کلید SSH با ssh-keygen، اتصال با کلید خصوصی، و بررسی پروسه‌های در حال اجرا (ps, netstat/ss) را یاد بگیر. سطح‌های ۱۵ تا ۱۸ Bandit را حل کن.",
  [R("Bandit Level 15", "https://overthewire.org/wargames/bandit/bandit15.html")],
  hours=2, kind="practice")

d(p1, "Cron jobs، Setuid و اسکریپت‌نویسی ساده",
  "مفهوم cron، فایل‌های setuid، و تفاوت اجرای یک باینری با یوزرهای مختلف را بفهم. سطح‌های ۱۹ تا ۲۳ Bandit را حل کن.",
  [R("Bandit Level 19", "https://overthewire.org/wargames/bandit/bandit19.html")],
  hours=2, kind="practice")

d(p1, "Netcat و ارتباط شبکه‌ای پایه",
  "با nc (netcat) کار کن: باز کردن پورت گوش‌ده، ارسال/دریافت داده، و شبیه‌سازی یک کلاینت-سرور ساده. سطح‌های ۲۴ تا ۲۷ Bandit را حل کن.",
  [R("Bandit Level 24", "https://overthewire.org/wargames/bandit/bandit24.html"),
   R("راهنمای Netcat", "https://linuxjourney.com/lesson/netcat-nc-command")],
  hours=2, kind="practice")

d(p1, "Git از دید امنیتی و باینری‌های غیرمعمول",
  "تاریخچهٔ Git، مخازن .git افشاشده، و بازیابی داده از commit های قدیمی را یاد بگیر — این مهارت مستقیماً در باگ‌بانتی برای پیدا کردن .git/ افشاشده کاربرد دارد. سطح‌های ۲۸ تا ۳۱ Bandit را حل کن.",
  [R("Bandit Level 28", "https://overthewire.org/wargames/bandit/bandit28.html")],
  hours=2, kind="practice")

d(p1, "Bandit — سطح ۳۲ تا ۳۳ و جمع‌بندی",
  "آخرین سطح‌های Bandit را تمام کن. سپس یک صفحهٔ خلاصه در Obsidian بنویس: کدام دستورات لینوکس را یاد گرفتی و در کدام سناریوها به کارت می‌آیند.",
  [R("Bandit Level 32", "https://overthewire.org/wargames/bandit/bandit32.html")],
  hours=2, kind="review")

d(p1, "Bash Scripting — مبانی",
  "متغیرها، حلقه‌ها (for/while)، شرط‌ها (if) و آرگومان‌های ورودی در Bash را تمرین کن. سه اسکریپت کوچک بنویس: یکی برای شمارش فایل‌ها، یکی برای پینگ گرفتن از چند IP، یکی برای پارس کردن یک فایل متنی.",
  [R("Bash Scripting — دورهٔ رایگان GitHub", "https://github.com/Idnan/bash-guide"),
   R("Learn Shell — تعاملی و رایگان", "https://www.learnshell.org/")],
  hours=3, kind="learn")

d(p1, "Bash Scripting — پیشرفته برای اتوماسیون هک",
  "کار با آرایه‌ها، توابع، و پایپ‌لاین دستورات (|, xargs, tee) را یاد بگیر. یک اسکریپت بنویس که یک لیست از دامنه را می‌گیرد و برایشان curl می‌زند و کد وضعیت HTTP را چاپ می‌کند — این پایهٔ اسکریپت‌های Recon آینده‌ات است.",
  [R("explainshell.com — تحلیل تعاملی هر دستور شل (رایگان)", "https://explainshell.com/")],
  hours=3, kind="practice")

d(p1, "TryHackMe: Linux Fundamentals 2 و 3 (رایگان)",
  "دو روم بعدی Linux Fundamentals را کامل کن: مدیریت پکیج (apt), سرویس‌ها (systemctl), و ویرایشگر متنی (nano/vim).",
  [R("Linux Fundamentals Part 2", "https://tryhackme.com/room/linuxfundamentalspart2"),
   R("Linux Fundamentals Part 3", "https://tryhackme.com/room/linuxfundamentalspart3")],
  hours=3, kind="practice")

d(p1, "مرور و آزمون خودت: لینوکس",
  "بدون نگاه کردن به یادداشت، سعی کن ۱۰ دستور مهم لینوکس که یاد گرفتی را از حفظ بنویسی و کاربردشان را توضیح دهی. هر جا گیر کردی، همان مبحث را دوباره مرور کن.",
  [R("Linux Journey — مرور کامل", "https://linuxjourney.com/")],
  hours=1, kind="review")

# ===========================================================================
# فاز ۲ — شبکه و HTTP
# ===========================================================================
p2 = phase("p2", "شبکه و پروتکل HTTP", "وب روی HTTP اجرا می‌شود؛ اگر HTTP را نفهمی، هیچ آسیب‌پذیری وب را هم نمی‌فهمی", "🌐", "#2563eb")

d(p2, "مدل OSI و TCP/IP",
  "لایه‌های OSI و TCP/IP، تفاوت TCP و UDP، و مفهوم پورت را یاد بگیر. جدول ۷ لایهٔ OSI را از حفظ در Obsidian بنویس.",
  [R("TryHackMe — Pre Security Path (رایگان)", "https://tryhackme.com/path/outline/presecurity")],
  hours=2, kind="learn")

d(p2, "DNS از صفر",
  "نحوهٔ کار DNS، انواع رکورد (A, AAAA, CNAME, MX, TXT, NS) و ابزار dig/nslookup را یاد بگیر و روی چند دامنهٔ واقعی تست کن.",
  [R("Cloudflare — DNS چیست (رایگان)", "https://www.cloudflare.com/learning/dns/what-is-dns/"),
   R("TryHackMe — DNS in Detail", "https://tryhackme.com/room/dnsindetail")],
  hours=2, kind="learn")

d(p2, "HTTP از صفر — متدها و کدهای وضعیت",
  "متدهای GET/POST/PUT/DELETE/PATCH/OPTIONS/HEAD، ساختار Request/Response، و کدهای وضعیت (2xx تا 5xx) را با MDN کامل بخوان.",
  [R("MDN — HTTP Overview (رایگان)", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"),
   R("MDN — HTTP Status Codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status")],
  hours=2, kind="learn")

d(p2, "هدرهای HTTP و کوکی‌ها",
  "هدرهای مهم امنیتی (Cookie, Set-Cookie, Authorization, Content-Type, Host, Referer, Origin, CSP, HSTS) را بشناس. یک سایت واقعی را با Burp یا DevTools باز کن و همهٔ هدرهای یک درخواست را شناسایی کن.",
  [R("MDN — HTTP Headers", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers"),
   R("MDN — HTTP Cookies", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies")],
  hours=2, kind="learn")

d(p2, "نصب و راه‌اندازی Burp Suite Community",
  "Burp Suite نسخهٔ رایگان (Community) را نصب کن، پروکسی مرورگر را روی آن تنظیم کن، گواهی CA آن را نصب کن، و اولین ترافیک HTTPS خودت را رهگیری کن.",
  [R("دانلود Burp Suite Community (رایگان)", "https://portswigger.net/burp/communitydownload"),
   R("PortSwigger — راه‌اندازی Burp با فایرفاکس", "https://portswigger.net/burp/documentation/desktop/getting-started")],
  hours=2, kind="practice")

d(p2, "کار عملی با Burp Suite: Proxy و Repeater",
  "تب Proxy و Repeater را با یک سایت تست (مثل PortSwigger labs) تمرین کن: رهگیری درخواست، ارسال به Repeater، تغییر پارامترها و ارسال دوباره.",
  [R("PortSwigger Academy — Burp Suite Essentials", "https://portswigger.net/web-security/learning-path")],
  hours=2, kind="practice")

d(p2, "HTTPS/TLS به زبان ساده",
  "Handshake TLS، گواهی دیجیتال، و چرا HTTPS مانع رهگیری ساده می‌شود را بفهم (نه در عمق ریاضی، در حد فهم مفهومی برای هک وب).",
  [R("Cloudflare — TLS چیست (رایگان)", "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/")],
  hours=1, kind="learn")

d(p2, "REST API و JSON",
  "مفهوم API، REST، و فرمت JSON را یاد بگیر. با Burp یک API عمومی رایگان (مثل JSONPlaceholder) را تست کن و درخواست‌های GET/POST را در Repeater بازسازی کن.",
  [R("JSONPlaceholder — API تست رایگان", "https://jsonplaceholder.typicode.com/"),
   R("MDN — Working with JSON", "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON")],
  hours=2, kind="practice")

d(p2, "وب‌سرورها: Apache و Nginx",
  "تفاوت Apache و Nginx، مفهوم Virtual Host، Reverse Proxy، و فایل‌های پیکربندی پایه را یاد بگیر — این دانش برای درک SSRF و Request Smuggling بعداً حیاتی است.",
  [R("DigitalOcean — مقایسهٔ رایگان Apache vs Nginx", "https://www.digitalocean.com/community/tutorials/apache-vs-nginx-practical-considerations"),
   R("Nginx — مستندات رسمی (رایگان)", "https://nginx.org/en/docs/")],
  hours=2, kind="learn")

d(p2, "Wireshark و تحلیل ترافیک شبکه",
  "Wireshark را نصب کن و یک کپچر ساده از ترافیک مرورگرت بگیر. بسته‌های HTTP و DNS را در آن پیدا و بررسی کن.",
  [R("دانلود Wireshark (رایگان)", "https://www.wireshark.org/download.html"),
   R("TryHackMe — Wireshark: The Basics", "https://tryhackme.com/room/wiresharkthebasics")],
  hours=2, kind="practice")

d(p2, "Nmap: اسکن پورت و سرویس",
  "اسکن پایه با nmap (-sV, -sC, -p-) روی یک هدف مجاز (مثل scanme.nmap.org) را تمرین کن و خروجی را تفسیر کن.",
  [R("Nmap — راهنمای رسمی (رایگان)", "https://nmap.org/book/man.html")],
  hours=2, kind="practice")

d(p2, "TryHackMe: Web Fundamentals — How the Web Works",
  "روم شروع مسیر Web Fundamentals را کامل کن: مرورگرها، سرورها و چرخهٔ کامل یک درخواست وب را از دید امنیتی مرور کن.",
  [R("TryHackMe — How Websites Work (رایگان)", "https://tryhackme.com/room/howwebsiteswork")],
  hours=2, kind="practice")

d(p2, "پروژهٔ کوچک: نقشهٔ کامل یک درخواست HTTP",
  "یک دیاگرام دستی (روی کاغذ یا Excalidraw) بکش که مسیر کامل یک کلیک کاربر تا برگشتن پاسخ را نشان دهد: DNS → TCP Handshake → TLS → HTTP Request → سرور → Response → رندر مرورگر. این تمرین درک عمیق‌تری از سطح حمله به تو می‌دهد.",
  [R("Excalidraw (رایگان، آنلاین)", "https://excalidraw.com/")],
  hours=2, kind="review")

# ===========================================================================
# فاز ۳ — برنامه‌نویسی برای هکرها
# ===========================================================================
p3 = phase("p3", "برنامه‌نویسی برای هکرها", "پایتون برای اسکریپت و اتوماسیون، جاوااسکریپت برای فهم و اکسپلویت سمت کلاینت", "🐍", "#d97706")

d(p3, "پایتون: متغیرها، انواع داده، شرط‌ها",
  "فصل‌های ۱ تا ۳ کتاب رایگان Automate the Boring Stuff را بخوان و تمرین‌هایش را کدنویسی کن.",
  [R("Automate the Boring Stuff with Python (کتاب کامل رایگان آنلاین)", "https://automatetheboringstuff.com/"),
   R("Python for Everybody — py4e (رایگان)", "https://www.py4e.com/")],
  hours=3, kind="learn")

d(p3, "پایتون: حلقه‌ها و توابع",
  "حلقه‌های for/while و نوشتن توابع را تمرین کن. یک اسکریپت بساز که یک لیست کلمه را می‌خواند و برای هرکدام یک عملیات ساده انجام می‌دهد (مثل ساخت پرمیوتیشن‌های ورودی).",
  [R("Automate the Boring Stuff — فصل توابع", "https://automatetheboringstuff.com/2e/chapter3/")],
  hours=3, kind="practice")

d(p3, "پایتون: لیست، دیکشنری و کار با فایل",
  "لیست‌ها، دیکشنری‌ها، و خواندن/نوشتن فایل متنی را یاد بگیر. یک اسکریپت بنویس که یک wordlist را از فایل می‌خواند و خط‌های تکراری را حذف می‌کند.",
  [R("Automate the Boring Stuff — فصل فایل‌ها", "https://automatetheboringstuff.com/2e/chapter9/")],
  hours=3, kind="practice")

d(p3, "پایتون: کتابخانهٔ requests",
  "با requests یک درخواست GET و POST به یک API واقعی بزن، هدر و کوکی سفارشی ست کن، و JSON پاسخ را پارس کن.",
  [R("مستندات requests (رایگان)", "https://requests.readthedocs.io/en/latest/user/quickstart/")],
  hours=3, kind="practice")

d(p3, "پروژهٔ پایتون: اسکنر ساب‌دامین ساده",
  "با requests و یک wordlist کوچک، اسکریپتی بنویس که چند ساب‌دامین رایج (www, api, dev, staging) را روی یک دامنهٔ تستی چک کند و وضعیت HTTP هرکدام را چاپ کند.",
  [R("SecLists — لیست‌های آماده برای Recon (رایگان، GitHub)", "https://github.com/danielmiessler/SecLists")],
  hours=3, kind="practice")

d(p3, "پروژهٔ پایتون: چک‌کنندهٔ لینک‌های شکسته/باز",
  "اسکریپت قبلی را توسعه بده تا هم‌زمانی (با threading یا concurrent.futures) اجرا شود تا سرعت بگیرد — این پایهٔ نوشتن ابزارهای Recon شخصی توست.",
  [R("Python concurrent.futures — مستندات رسمی", "https://docs.python.org/3/library/concurrent.futures.html")],
  hours=3, kind="practice")

d(p3, "جاوااسکریپت: مبانی زبان",
  "متغیرها (let/const)، توابع، شرط‌ها و حلقه‌ها در جاوااسکریپت را یاد بگیر — چون تمام منطق سمت کلاینت وب با همین زبان نوشته می‌شود.",
  [R("javascript.info — بخش اول (رایگان)", "https://javascript.info/first-steps")],
  hours=3, kind="learn")

d(p3, "جاوااسکریپت: DOM و رویدادها",
  "نحوهٔ دستکاری DOM، event listener ها، و innerHTML را بفهم — پایهٔ فهم XSS دقیقاً همین‌جاست.",
  [R("javascript.info — Document (رایگان)", "https://javascript.info/document"),
   R("MDN — Introduction to DOM", "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction")],
  hours=3, kind="learn")

d(p3, "جاوااسکریپت: Same-Origin Policy و Fetch/AJAX",
  "مفهوم Origin، Same-Origin Policy، و نحوهٔ کار fetch/XMLHttpRequest را یاد بگیر — این‌ها مستقیماً پایهٔ CORS و CSRF هستند.",
  [R("MDN — Same-origin policy", "https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy"),
   R("javascript.info — Fetch", "https://javascript.info/fetch")],
  hours=3, kind="learn")

d(p3, "SQL از صفر",
  "دستورات SELECT, WHERE, JOIN, UNION، و کامنت‌گذاری در SQL را با یک دیتابیس تمرینی رایگان یاد بگیر — پیش‌نیاز مطلق فهم SQL Injection.",
  [R("SQLBolt — تعاملی و رایگان", "https://sqlbolt.com/"),
   R("W3Schools SQL Tutorial (رایگان)", "https://www.w3schools.com/sql/")],
  hours=3, kind="learn")

d(p3, "Git و GitHub برای هکرها",
  "clone، commit، branch، و مهم‌تر از همه نحوهٔ جست‌وجوی سکرت‌های افشاشده (کلید API، پسورد) در تاریخچهٔ کامیت‌های عمومی گیت‌هاب را یاد بگیر.",
  [R("راهنمای رسمی Git (رایگان)", "https://git-scm.com/book/en/v2"),
   R("ابزار TruffleHog برای یافتن سکرت در گیت (رایگان)", "https://github.com/trufflesecurity/trufflehog")],
  hours=2, kind="learn")

d(p3, "پروژهٔ پایانی فاز: ابزار شخصی Recon نسخهٔ ۱",
  "همهٔ چیزهایی که در پایتون یاد گرفتی را ترکیب کن و اولین نسخهٔ ابزار Recon شخصی‌ات را بساز: گرفتن یک دامنه، چک کردن چند ساب‌دامین رایج، و ذخیرهٔ خروجی در یک فایل CSV. این ابزار را در طول مسیر توسعه می‌دهی.",
  [R("مخزن GitHub خودت را بساز و کد را همان‌جا نگه‌دار", "https://github.com/")],
  hours=3, kind="milestone")

d(p3, "مرور فاز برنامه‌نویسی",
  "بدون نگاه به کد قبلی، یک اسکریپت پایتون جدید از صفر بنویس که یک URL می‌گیرد، وضعیت HTTP را چک می‌کند و هدرهای پاسخ را چاپ می‌کند. اگر گیر کردی، دقیقاً همان بخش را مرور کن.",
  [R("Python Docs (رایگان)", "https://docs.python.org/3/")],
  hours=2, kind="review")

# ===========================================================================
# فاز ۴ — مبانی امنیت وب و Burp Suite حرفه‌ای
# ===========================================================================
p4 = phase("p4", "مبانی امنیت وب و Burp Suite حرفه‌ای", "قبل از شکار، باید روی نقشهٔ آسیب‌پذیری‌ها و ابزار اصلی‌ات مسلط شوی", "🛠️", "#dc2626")

d(p4, "OWASP Top 10 — نسخهٔ کامل",
  "لیست ۲۰۲۱ OWASP Top 10 را کامل بخوان و برای هرکدام یک خط توضیح به زبان خودت در Obsidian بنویس. این چارچوب مرجع کل مسیر آینده‌ات است.",
  [R("OWASP Top 10 (رایگان، رسمی)", "https://owasp.org/www-project-top-ten/")],
  hours=2, kind="learn")

d(p4, "معماری اپلیکیشن‌های وب مدرن",
  "تفاوت اپلیکیشن سنتی (Server-rendered) با SPA (React/Vue/Angular)، و نقش API در معماری مدرن را بفهم — چون سطح حمله در هرکدام فرق دارد.",
  [R("مقالهٔ رایگان دربارهٔ معماری SPA — MDN", "https://developer.mozilla.org/en-US/docs/Glossary/SPA")],
  hours=2, kind="learn")

d(p4, "Burp Suite: Intruder و Fuzzing پایه",
  "تب Intruder را با یک هدف تمرینی (DVWA یا PortSwigger labs) کار کن: Sniper، Payload types، و تحلیل نتایج بر اساس طول پاسخ.",
  [R("PortSwigger — Burp Intruder Documentation", "https://portswigger.net/burp/documentation/desktop/tools/intruder")],
  hours=2, kind="practice")

d(p4, "نصب DVWA برای تمرین محلی",
  "DVWA (Damn Vulnerable Web Application) را روی ماشین مجازی خودت با XAMPP/Docker بالا بیار — یک محیط تمرین کاملاً قانونی و محلی برای آزمایش تکنیک‌ها.",
  [R("DVWA — رایگان، GitHub", "https://github.com/digininja/DVWA"),
   R("راه‌اندازی DVWA با Docker (رایگان)", "https://github.com/digininja/DVWA#docker")],
  hours=2, kind="practice")

d(p4, "Burp Suite: Decoder، Comparer و Extensions",
  "Decoder را برای Base64/URL-encode یاد بگیر، Comparer را برای مقایسهٔ دو پاسخ تمرین کن، و از BApp Store چند اکستنشن رایگان (مثل Logger++) نصب کن.",
  [R("PortSwigger BApp Store (رایگان)", "https://portswigger.net/bappstore")],
  hours=2, kind="practice")

d(p4, "متدولوژی کلی تست نفوذ وب",
  "چرخهٔ کامل یک تست امنیتی وب (Recon → Mapping → Testing → Exploitation → Reporting) را از منابع رایگان Bugcrowd University یاد بگیر.",
  [R("Bugcrowd University — رایگان (GitHub)", "https://github.com/bugcrowd/bugcrowd_university")],
  hours=2, kind="learn")

d(p4, "شروع دورهٔ رایگان یاشار شاهین‌زاده در مکتب‌خونه",
  "دورهٔ «آموزش رایگان امنیت اپلیکیشن از صفر» یاشار شاهین‌زاده را در مکتب‌خونه پیدا کن، ثبت‌نام رایگان کن و شروع به دیدن کن.",
  [R("جست‌وجوی دوره در مکتب‌خونه", "https://maktabkhooneh.org/search/?q=%D8%A7%D9%85%D9%86%DB%8C%D8%AA+%D8%A7%D9%BE%D9%84%DB%8C%DA%A9%DB%8C%D8%B4%D9%86+%D8%A7%D8%B2+%D8%B5%D9%81%D8%B1"),
   R("پیج توییتر/ایکس یاشار برای اطلاع از دوره‌های جدید", "https://x.com/yshahinzadeh")],
  hours=2, kind="learn")

d(p4, "شروع Web Security Academy پورت‌سویگر — بخش Essential Skills",
  "قبل از رفتن سراغ آسیب‌پذیری‌ها، بخش Essential Skills آکادمی پورت‌سویگر را کامل کن تا با محیط لب‌ها و روش کار آکادمی آشنا شوی.",
  [R("PortSwigger Academy — Essential Skills", "https://portswigger.net/web-security/essential-skills")],
  hours=2, kind="practice")

d(p4, "ثبت‌نام در Hacker101 و شروع ویدیوها",
  "در Hacker101 ثبت‌نام کن (کاملاً رایگان، ساختهٔ HackerOne) و اولین ویدیوهای مقدماتی را ببین. این پلتفرم را در کنار PortSwigger در طول مسیر ادامه می‌دهی.",
  [R("Hacker101 (رایگان)", "https://www.hacker101.com/"),
   R("Hacker101 — بخش ویدیوها", "https://www.hacker101.com/videos")],
  hours=2, kind="learn")

d(p4, "مرور: نقشهٔ ذهنی کامل مسیر تا اینجا",
  "یک نقشهٔ ذهنی (mind map) از تمام چیزهایی که تا امروز یاد گرفتی بکش: لینوکس، شبکه، برنامه‌نویسی، ابزارها. این نقشه پایهٔ ورود به فاز آسیب‌پذیری‌هاست.",
  [R("XMind (رایگان)", "https://xmind.app/")],
  hours=1, kind="review")

# ===========================================================================
# فاز ۵ — OWASP Top 10 + PortSwigger Web Security Academy (هستهٔ اصلی)
# ===========================================================================
p5 = phase("p5", "هستهٔ آسیب‌پذیری‌های وب (PortSwigger Academy)", "قلب این نقشه‌راه؛ هر آسیب‌پذیری را تئوری + لب عملی رایگان پورت‌سویگر یاد می‌گیری", "🎯", "#be123c")

# ساختار: هر تاپیک پورت‌سویگر با ۱ تا ۳ روز، به ترتیب منطقی آموزشی (نه لزوماً ترتیب سایت)
swigger_topics = [
    ("SQL Injection", "sql-injection", 3, "پادشاه آسیب‌پذیری‌های سمت سرور؛ تمام ۱۸ لب را با دقت حل کن، از UNION-based تا Blind با تاخیر زمانی."),
    ("Cross-Site Scripting (XSS)", "cross-site-scripting", 4, "پرتکرارترین باگ در برنامه‌های باگ‌بانتی؛ Reflected، Stored و DOM-based را با تمام ۳۰ لب کار کن."),
    ("Cross-Site Request Forgery (CSRF)", "csrf", 2, "درک کامل CSRF token، SameSite cookie، و بای‌پس‌های رایج آن."),
    ("Cross-Origin Resource Sharing (CORS)", "cors", 1, "پیکربندی نادرست CORS و سرقت داده از طریق origin مخرب."),
    ("Clickjacking", "clickjacking", 1, "حملات لایه‌بندی UI و بای‌پس‌های X-Frame-Options/CSP."),
    ("Authentication", "authentication", 3, "باگ‌های لاگین، ریست پسورد، 2FA bypass، و رمزهای قابل حدس‌زدن."),
    ("Access Control (IDOR/Privilege Escalation)", "access-control", 3, "یکی از پرسودترین کلاس‌ها در باگ‌بانتی؛ IDOR و Broken Access Control را عمیق کار کن."),
    ("Path Traversal", "file-path-traversal", 1, "دسترسی به فایل‌های خارج از دایرکتوری وب‌روت."),
    ("Command Injection", "os-command-injection", 1, "اجرای دستور سیستم‌عامل از طریق ورودی کاربر."),
    ("Business Logic Vulnerabilities", "logic-flaws", 2, "باگ‌هایی که هیچ اسکنری پیدا نمی‌کند؛ فقط با فکر انسانی کشف می‌شوند."),
    ("Information Disclosure", "information-disclosure", 1, "افشای اطلاعات حساس از طریق پیام خطا، کامنت کد، یا فایل پشتیبان."),
    ("File Upload Vulnerabilities", "file-upload", 2, "آپلود وب‌شل، بای‌پس فیلتر پسوند/MIME-type."),
    ("Race Conditions", "race-conditions", 2, "بهره‌برداری از تایمینگ همزمان درخواست‌ها؛ مبحثی داغ و کم‌رقابت در باگ‌بانتی امروز."),
    ("Server-Side Request Forgery (SSRF)", "ssrf", 2, "واداشتن سرور به ارسال درخواست به مقصد دلخواه تو؛ اغلب مسیر ورود به شبکهٔ داخلی/کلاود."),
    ("XXE Injection", "xxe", 2, "آسیب‌پذیری XML External Entity و خواندن فایل سیستم از طریقش."),
    ("NoSQL Injection", "nosql-injection", 1, "تزریق در دیتابیس‌های NoSQL مثل MongoDB."),
    ("API Testing", "api-testing", 2, "متدولوژی تست API های REST؛ کشف اندپوینت‌های پنهان."),
    ("Web Cache Deception", "web-cache-deception", 1, "فریب کش برای ذخیرهٔ صفحات خصوصی به‌صورت عمومی."),
    ("WebSockets", "websockets", 1, "امنیت ارتباطات WebSocket و CSRF مشابه در WS."),
    ("DOM-based vulnerabilities", "dom-based", 2, "منابع (source) و مقصدهای (sink) خطرناک در جاوااسکریپت سمت کلاینت."),
    ("Insecure Deserialization", "deserialization", 2, "بهره‌برداری از deserialize کردن دادهٔ غیرقابل‌اعتماد در PHP/Java/.NET/Python."),
    ("GraphQL API Vulnerabilities", "graphql", 2, "Introspection، Batching attacks و IDOR در GraphQL."),
    ("Server-Side Template Injection (SSTI)", "server-side-template-injection", 2, "تزریق در موتورهای قالب (Jinja2, Twig, FreeMarker) که اغلب به RCE می‌رسد."),
    ("Web Cache Poisoning", "web-cache-poisoning", 2, "مسموم‌سازی کش برای تحویل محتوای مخرب به کاربران دیگر."),
    ("HTTP Host Header Attacks", "host-header", 1, "دستکاری هدر Host برای پویزنینگ کش، ریست پسورد مخرب، و روتینگ اشتباه."),
    ("HTTP Request Smuggling", "request-smuggling", 3, "یکی از پیچیده‌ترین و باارزش‌ترین کلاس‌های امروز؛ اختلاف تفسیر HTTP بین پروکسی و سرور."),
    ("OAuth Authentication", "oauth", 2, "باگ‌های رایج در پیاده‌سازی OAuth 2.0 و سرقت اکانت."),
    ("JWT Attacks", "jwt", 2, "دستکاری الگوریتم، کلید ضعیف، و بای‌پس امضای JSON Web Token."),
    ("Prototype Pollution", "prototype-pollution", 2, "آلوده‌سازی پروتوتایپ در جاوااسکریپت، سمت کلاینت و سمت سرور (Node.js)."),
    ("Web LLM Attacks", "llm-attacks", 1, "کلاس نوظهور: Prompt Injection و آسیب‌پذیری اپلیکیشن‌های مبتنی بر LLM."),
]

for name_fa, slug, ndays, desc in swigger_topics:
    for i in range(ndays):
        part = f" — بخش {i+1} از {ndays}" if ndays > 1 else ""
        d(p5, f"{name_fa}{part}",
          f"{desc} تمام لب‌های عملی «{name_fa}» را در آکادمی پورت‌سویگر با تلاش شخصی حل کن؛ اگر بعد از ۳۰ دقیقه گیر کردی، فقط hint را نگاه کن نه جواب کامل را. برای هر آسیب‌پذیری که حل می‌کنی یک خلاصه (چی بود، چطور پیدا شد، چطور fix می‌شود) در Obsidian بنویس.",
          [R(f"PortSwigger Academy — {name_fa}", f"https://portswigger.net/web-security/{slug}"),
           R("PayloadsAllTheThings — پیلود آماده برای این کلاس آسیب‌پذیری", "https://github.com/swisskyrepo/PayloadsAllTheThings")],
          hours=3, kind="practice")

d(p5, "مرور بزرگ: بازسازی تمام آسیب‌پذیری‌ها روی DVWA",
  "روی DVWA محلی خودت، حداقل یک نمونه از هر کلاس آسیب‌پذیری که یاد گرفتی (SQLi, XSS, CSRF, IDOR, SSRF...) را از صفر و بدون نگاه به یادداشت پیاده کن.",
  [R("DVWA (رایگان)", "https://github.com/digininja/DVWA")],
  hours=3, kind="review")

d(p5, "چک‌پوینت بزرگ: امتحان جامع Web Security Academy",
  "به بخش «All Topics» آکادمی پورت‌سویگر برگرد و هر لبی که هنوز حل‌نشده مانده را تمام کن. هدف: نوار پیشرفت Academy تو باید به بالای ۸۰٪ برسد.",
  [R("PortSwigger — All Topics", "https://portswigger.net/web-security/all-topics")],
  hours=3, kind="milestone")

# ===========================================================================
# فاز ۶ — تمرین متمرکز فارسی (Voorivex) + Hacker101 CTF
# ===========================================================================
p6 = phase("p6", "تمرین متمرکز: Voorivex و Hacker101 CTF", "حالا وقتشه تئوری رو با محتوای فارسی تخصصی و یک CTF واقعی محک بزنی", "🕹️", "#0891b2")

d(p6, "دورهٔ رایگان یاشار شاهین‌زاده — تکمیل",
  "دورهٔ «آموزش رایگان امنیت اپلیکیشن از صفر» در مکتب‌خونه را تمام کن. هر مفهومی که تکرار شنیدی ولی هنوز مطمئن نیستی، دوباره در PortSwigger جست‌وجو کن.",
  [R("دورهٔ رایگان یاشار در مکتب‌خونه", "https://maktabkhooneh.org/search/?q=%D8%A7%D9%85%D9%86%DB%8C%D8%AA+%D8%A7%D9%BE%D9%84%DB%8C%DA%A9%DB%8C%D8%B4%D9%86+%D8%A7%D8%B2+%D8%B5%D9%81%D8%B1")],
  hours=3, kind="learn")

d(p6, "بلاگ و شبکه‌های Voorivex Team را زیر و رو کن",
  "تمام پست‌های فنی بلاگ Voorivex Team را بخوان و در توییتر/ایکس یاشار شاهین‌زاده دنبالش کن؛ نکات تازه یا write-up های او را یادداشت کن.",
  [R("بلاگ Voorivex Team", "https://blog.voorivex.team/"),
   R("ایکس یاشار شاهین‌زاده", "https://x.com/yshahinzadeh")],
  hours=2, kind="learn")

d(p6, "بررسی آکادمی Voorivex برای دوره‌های رایگان/تخفیف‌دار جدید",
  "به سایت آکادمی Voorivex سر بزن، دوره‌های فعلی (مثل OWASP Zero) را ببین و اگر بخش رایگان یا کد تخفیف دانشجویی دارد ثبت‌نام کن؛ در غیر این‌صورت محتوای رایگان یوتیوبشان را دنبال کن.",
  [R("آکادمی Voorivex", "https://voorivex.academy/"),
   R("کانال یوتیوب Voorivex", "https://www.youtube.com/@Voorivex")],
  hours=1, kind="learn")

d(p6, "Hacker101 CTF — ثبت‌نام و اولین چالش",
  "در Hacker101 CTF ثبت‌نام کن و اولین چالش (معمولاً ساده‌ترین levelها) را بدون کمک بیرونی حل کن.",
  [R("Hacker101 CTF (رایگان)", "https://ctf.hacker101.com/")],
  hours=3, kind="practice")

d(p6, "Hacker101 CTF — چالش‌های سطح ۲",
  "به چالش‌های پیچیده‌تر Hacker101 CTF برو. هر چالش را حل‌شده یا نشده، در Obsidian با جزئیات کامل مستند کن (این تمرین مستقیم برای نوشتن گزارش حرفه‌ای است).",
  [R("Hacker101 CTF", "https://ctf.hacker101.com/")],
  hours=3, kind="practice")

d(p6, "Hacker101 CTF — چالش‌های سطح پیشرفته",
  "روی سخت‌ترین چالش‌های باقی‌مانده کار کن. اگر بعد از تلاش جدی گیر کردی، Hacker101 write-up های عمومی را جست‌وجو کن و فقط بعد از تلاش خودت بخوان.",
  [R("Hacker101 — بخش Resources", "https://www.hacker101.com/resources")],
  hours=3, kind="practice")

d(p6, "Google XSS Game و Google Gruyere",
  "دو محیط تمرین رایگان گوگل را حل کن؛ XSS Game تمرکز ویژه روی XSS دارد و Gruyere یک اپ کامل آسیب‌پذیر با چالش‌های متنوع است.",
  [R("Google XSS Game (رایگان)", "https://xss-game.appspot.com/"),
   R("Google Gruyere (رایگان)", "https://google-gruyere.appspot.com/")],
  hours=3, kind="practice")

d(p6, "PentesterLab — Web for Pentester (رایگان)",
  "لب رایگان «Web for Pentester» پنترستر‌لب را دانلود و روی ماشین مجازی اجرا کن؛ مجموعه‌ای متمرکز از آسیب‌پذیری‌های کلاسیک وب.",
  [R("PentesterLab — Web for Pentester (رایگان)", "https://pentesterlab.com/exercises/web_for_pentester")],
  hours=3, kind="practice")

d(p6, "Bugcrowd University — ویدیوها و لب‌ها",
  "ماژول‌های ویدیویی Bugcrowd University را که هنوز ندیده‌ای تماشا کن، خصوصاً بخش‌های XSS، Access Control و Burp Suite.",
  [R("Bugcrowd University (رایگان)", "https://github.com/bugcrowd/bugcrowd_university")],
  hours=2, kind="learn")

d(p6, "کانال یوتیوب Rana Khalil — سری Web Security Academy",
  "پلی‌لیست رایگان Rana Khalil که هر لب PortSwigger را با ویدیو حل می‌کند را برای لب‌هایی که خودت سخت حل کردی تماشا کن — روش فکری متفاوتی یاد می‌گیری.",
  [R("کانال یوتیوب Rana Khalil", "https://www.youtube.com/@RanaKhalil101")],
  hours=2, kind="learn")

d(p6, "کانال یوتیوب NahamSec — ویدیوهای شکار زنده (Live Hacking)",
  "چند ویدیوی «Live Hacking» رایگان NahamSec را ببین تا فرایند فکری واقعی یک هانتر حرفه‌ای هنگام شکار روی برنامهٔ واقعی را از نزدیک ببینی.",
  [R("کانال یوتیوب NahamSec", "https://www.youtube.com/@NahamSec")],
  hours=2, kind="learn")

d(p6, "OverTheWire Natas — سطح ۰ تا ۷ (وارگیم اختصاصی وب)",
  "برخلاف Bandit که لینوکس‌محور بود، Natas مستقیماً روی آسیب‌پذیری‌های وب (View Source، PHP، کوکی، هدرها) تمرکز دارد. سطح‌های ۰ تا ۷ را با مرورگر و View-Source حل کن.",
  [R("OverTheWire Natas (رایگان)", "https://overthewire.org/wargames/natas/")],
  hours=3, kind="practice")

d(p6, "OverTheWire Natas — سطح ۸ تا ۱۵",
  "سطح‌های میانی Natas را حل کن: بای‌پس مقایسهٔ نوع در PHP، تزریق دستور، و باگ‌های منطقی ساده در کد PHP.",
  [R("OverTheWire Natas (رایگان)", "https://overthewire.org/wargames/natas/")],
  hours=3, kind="practice")

d(p6, "HackTheBox — ساخت حساب رایگان و Starting Point Tier 0",
  "در Hack The Box با حساب رایگان (Free tier، بدون نیاز به VIP) ثبت‌نام کن و ماشین‌های Tier 0 مسیر Starting Point را حل کن؛ هر ماشین یک راهنمای رسمی گام‌به‌گام رایگان دارد.",
  [R("Hack The Box — Starting Point (رایگان)", "https://app.hackthebox.com/starting-point"),
   R("راهنمای شروع Starting Point", "https://help.hackthebox.com/en/articles/6007919-introduction-to-starting-point")],
  hours=3, kind="practice")

d(p6, "HackTheBox — Starting Point Tier 1",
  "به ماشین‌های Tier 1 برو؛ کمی پیچیده‌تر از Tier 0 هستند و مهارت شمارش سرویس (enumeration) و ترکیب چند آسیب‌پذیری را تقویت می‌کنند.",
  [R("Hack The Box — Starting Point (رایگان)", "https://app.hackthebox.com/starting-point")],
  hours=3, kind="practice")

d(p6, "مرور و جمع‌بندی فاز: پورتفولیوی حل‌شده‌ها",
  "لیستی از تمام چالش‌ها/لب‌هایی که تا الان حل کردی (Bandit, PortSwigger, Hacker101, DVWA, PentesterLab, Gruyere) را در یک صفحهٔ «Portfolio» در Obsidian جمع کن — این سند پایهٔ رزومهٔ آینده‌ات است.",
  [R("نمونه ساختار پورتفولیو امنیتی (رایگان، GitHub)", "https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters")],
  hours=2, kind="review")

# ===========================================================================
# فاز ۷ — Recon و متدولوژی شکار باگ
# ===========================================================================
p7 = phase("p7", "Recon و متدولوژی حرفه‌ای شکار", "قبل از تست هر آسیب‌پذیری، باید سطح حمله را کامل نقشه‌برداری کنی", "🔭", "#4d7c0f")

d(p7, "متدولوژی Jason Haddix — Bug Hunter's Methodology (نسخهٔ کامل)",
  "ویدیوی کامل ۲ ساعتهٔ Jason Haddix را با یادداشت‌برداری کامل ببین؛ این یکی از معتبرترین متدولوژی‌های رایگان موجود در دنیای باگ‌بانتی است.",
  [R("The Bug Hunter's Methodology — ویدیوی کامل ۲ ساعته (رایگان)", "https://www.youtube.com/watch?v=uKWu6yhnhbQ")],
  hours=3, kind="learn")

d(p7, "Bug Hunter's Methodology v4 — Recon Edition",
  "نسخهٔ تخصصی Recon این متدولوژی را ببین و لیست کامل ابزارهایی که معرفی می‌کند را در Obsidian یادداشت کن.",
  [R("Bug Hunter's Methodology v4.0 — Recon Edition (رایگان)", "https://www.youtube.com/watch?v=p4JgIu1mceI")],
  hours=2, kind="learn")

d(p7, "Subdomain Enumeration — ابزارها",
  "ابزارهای رایگان subfinder و amass را نصب کن و روی یک دامنهٔ دارای برنامهٔ باگ‌بانتی عمومی (طبق قوانین برنامه) اجرا کن؛ خروجی‌ها را مقایسه کن.",
  [R("subfinder (رایگان، ProjectDiscovery)", "https://github.com/projectdiscovery/subfinder"),
   R("OWASP Amass (رایگان)", "https://github.com/owasp-amass/amass")],
  hours=3, kind="practice")

d(p7, "پروب کردن زنده‌بودن هاست: httpx",
  "httpx را نصب کن و لیست ساب‌دامین‌های قبلی را برایش پایپ کن تا مشخص شود کدام‌ها زنده‌اند، کد وضعیت و تکنولوژی هرکدام چیست.",
  [R("httpx (رایگان، ProjectDiscovery)", "https://github.com/projectdiscovery/httpx")],
  hours=2, kind="practice")

d(p7, "اسکن آسیب‌پذیری خودکار: nuclei",
  "nuclei را نصب کن، template های عمومی رایگانش را آپدیت کن، و روی هدف‌های مجاز (طبق scope برنامه) اجرا کن؛ نتایج false-positive را یاد بگیر تشخیص بدهی.",
  [R("nuclei (رایگان، ProjectDiscovery)", "https://github.com/projectdiscovery/nuclei")],
  hours=3, kind="practice")

d(p7, "کشف محتوا و مسیر: ffuf و دیکشنری‌ها",
  "ffuf را برای Directory/Content Discovery با wordlist های SecLists تمرین کن؛ فرق fuzzing پارامتر، مسیر، و ساب‌دامین را در عمل ببین.",
  [R("ffuf (رایگان)", "https://github.com/ffuf/ffuf"),
   R("SecLists — دیکشنری‌های آماده (رایگان)", "https://github.com/danielmiessler/SecLists")],
  hours=3, kind="practice")

d(p7, "ابزارهای Tomnomnok و ترکیب پایپ‌لاین Recon",
  "ابزارهای سبک و کاربردی tomnomnom (مثل waybackurls, gf, httprobe) را نصب کن و یک پایپ‌لاین ترکیبی بساز: subfinder | httpx | nuclei.",
  [R("ابزارهای tomnomnom (رایگان)", "https://github.com/tomnomnom"),
   R("waybackurls — کشف URL از آرشیو وب (رایگان)", "https://github.com/tomnomnom/waybackurls")],
  hours=3, kind="practice")

d(p7, "Google Dorking و OSINT پیشرفته",
  "تکنیک‌های Google Dork (site:, inurl:, filetype:) و OSINT برای پیدا کردن فایل‌های حساس افشاشده، پنل‌های ادمین، و ساب‌دامین‌های فراموش‌شده را یاد بگیر.",
  [R("Google Hacking Database — GHDB (رایگان)", "https://www.exploit-db.com/google-hacking-database")],
  hours=2, kind="practice")

d(p7, "شناسایی تکنولوژی و اثرانگشت‌گیری",
  "ابزارهای Wappalyzer و whatweb را برای شناسایی فریم‌ورک، CMS و کتابخانه‌های استفاده‌شده در یک هدف تمرین کن؛ دانستن نسخهٔ دقیق فناوری مسیر مستقیم به CVEهای شناخته‌شده است.",
  [R("Wappalyzer (افزونهٔ رایگان مرورگر)", "https://www.wappalyzer.com/"),
   R("whatweb (رایگان)", "https://github.com/urbanadventurer/WhatWeb")],
  hours=2, kind="practice")

d(p7, "ساخت پایپ‌لاین Recon شخصی نسخهٔ نهایی",
  "ابزار پایتون خودت از فاز ۳ را با ابزارهای جدید (subfinder, httpx, nuclei) ترکیب کن و یک اسکریپت Bash یا Python بساز که با یک دستور، کل مراحل Recon اولیه را روی یک دامنهٔ ورودی اجرا کند.",
  [R("مخزن الگوی Recon خودکار (رایگان، GitHub)", "https://github.com/six2dez/reconftw")],
  hours=3, kind="milestone")

d(p7, "انتخاب اولین برنامهٔ باگ‌بانتی هدف",
  "بر اساس Scope، حجم رقابت و نوع اپلیکیشن، یک برنامهٔ باگ‌بانتی واقعی (روی HackerOne/Bugcrowd) یا یک VDP انتخاب کن که قصد داری در فازهای بعد رویش تمرکز کنی. قوانین Scope و Rules of Engagement را کامل بخوان.",
  [R("HackerOne — Directory برنامه‌ها", "https://hackerone.com/directory/programs"),
   R("Bugcrowd — Programs", "https://bugcrowd.com/programs")],
  hours=2, kind="review")

d(p7, "اولین دور Recon کامل روی هدف واقعی",
  "پایپ‌لاین Recon خودت را روی برنامهٔ هدف انتخابی اجرا کن (فقط در محدودهٔ Scope مجاز). نتایج را در Obsidian دسته‌بندی کن: ساب‌دامین‌ها، تکنولوژی‌ها، اندپوینت‌های API، و نقاط ورودی مشکوک.",
  [R("چک‌لیست Recon — Bug Bounty Roadmap Voorivex", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")],
  hours=3, kind="practice")

# ===========================================================================
# فاز ۸ — امنیت موبایل و API/GraphQL
# ===========================================================================
p8 = phase("p8", "امنیت موبایل و API پیشرفته", "بسیاری از برنامه‌های باگ‌بانتی امروز اپ موبایل و API را هم شامل می‌شوند؛ رقابت کمتر، پاداش اغلب بیشتر", "📱", "#9333ea")

d(p8, "معرفی OWASP MASVS/MASTG",
  "استاندارد OWASP Mobile Application Security (MASVS) و راهنمای تست آن (MASTG) را به‌عنوان نقشهٔ راه امنیت موبایل مرور کن.",
  [R("OWASP MASTG (رایگان)", "https://mas.owasp.org/MASTG/")],
  hours=2, kind="learn")

d(p8, "راه‌اندازی محیط تست اندروید",
  "Android Studio و یک AVD (شبیه‌ساز اندروید) رایگان را نصب کن، ADB را یاد بگیر، و یک اپ آسیب‌پذیر تمرینی (AndroGoat) را روی شبیه‌ساز نصب کن.",
  [R("AndroGoat — اپ تمرینی رایگان (GitHub)", "https://github.com/satishpatnayak/AndroGoat"),
   R("Android Studio (رایگان)", "https://developer.android.com/studio")],
  hours=3, kind="practice")

d(p8, "رهگیری ترافیک اپ موبایل با Burp",
  "Burp Suite را به‌عنوان پروکسی روی شبیه‌ساز اندروید تنظیم کن، گواهی CA را نصب کن، و ترافیک اپ AndroGoat را رهگیری کن — همان تکنیکی که برای تست هر اپ موبایل واقعی به کار می‌بری.",
  [R("PortSwigger — پیکربندی Burp برای موبایل", "https://portswigger.net/burp/documentation/desktop/mobile")],
  hours=3, kind="practice")

d(p8, "دیکامپایل و تحلیل استاتیک اپ اندروید",
  "با jadx یک فایل APK را دیکامپایل کن و به‌دنبال سکرت‌های هاردکد شده (API Key، آدرس سرور، پسورد) در کد بگرد.",
  [R("jadx — دیکامپایلر رایگان اندروید", "https://github.com/skylot/jadx")],
  hours=3, kind="practice")

d(p8, "Insecure Data Storage و SSL Pinning Bypass",
  "بررسی کن اپ چه داده‌ای را ناامن ذخیره می‌کند (SharedPreferences، دیتابیس محلی)، و مفهوم SSL Pinning و روش‌های رایگان bypass آن (Frida/Objection) را یاد بگیر.",
  [R("OWASP MASTG — Testing Network Communication", "https://github.com/OWASP/mastg/blob/master/Document/0x05g-Testing-Network-Communication.md"),
   R("Objection (رایگان)", "https://github.com/sensepost/objection")],
  hours=3, kind="practice")

d(p8, "OWASP API Security Top 10",
  "لیست ۲۰۲۳ OWASP API Security Top 10 را کامل بخوان — نقشهٔ راه اختصاصی آسیب‌پذیری‌های API که امروز در باگ‌بانتی بسیار پرارزش است.",
  [R("OWASP API Security Project (رایگان)", "https://owasp.org/www-project-api-security/")],
  hours=2, kind="learn")

d(p8, "BOLA/IDOR در APIها",
  "Broken Object Level Authorization (BOLA) — رایج‌ترین باگ API در دنیای واقعی — را با لب‌های عملی PortSwigger تمرین کن.",
  [R("PortSwigger — API Testing Labs", "https://portswigger.net/web-security/api-testing")],
  hours=3, kind="practice")

d(p8, "GraphQL Security عمیق",
  "Introspection query، حملات Batching، و IDOR در GraphQL را با لب‌های رایگان پورت‌سویگر عمیق‌تر تمرین کن.",
  [R("PortSwigger — GraphQL API vulnerabilities", "https://portswigger.net/web-security/graphql")],
  hours=3, kind="practice")

d(p8, "APIsec University — دوره‌های رایگان API Security",
  "دوره‌های رایگان APIsec University را ببین، خصوصاً دورهٔ مقدماتی API Penetration Testing.",
  [R("APIsec University (رایگان با ثبت‌نام)", "https://www.apisecuniversity.com/")],
  hours=2, kind="learn")

d(p8, "پروژهٔ فاز: تست کامل یک API عمومی رایگان",
  "با Postman یا Burp یک API عمومی تست (مثل یک اپ نمونهٔ OWASP juice-shop) را کامل بررسی کن: تمام اندپوینت‌ها را کشف کن، احراز هویت را بشکن، و به‌دنبال BOLA بگرد.",
  [R("OWASP Juice Shop — اپ کاملاً آسیب‌پذیر تمرینی (رایگان)", "https://owasp.org/www-project-juice-shop/")],
  hours=3, kind="milestone")

# ===========================================================================
# فاز ۹ — شکار واقعی، گزارش‌نویسی و پورتفولیو
# ===========================================================================
p9 = phase("p9", "شکار واقعی و گزارش‌نویسی حرفه‌ای", "از این‌جا به بعد روی برنامه‌های واقعی کار می‌کنی؛ کیفیت گزارش به‌اندازهٔ خود باگ اهمیت دارد", "🏹", "#b45309")

d(p9, "آناتومی یک گزارش حرفه‌ای باگ‌بانتی",
  "ساختار استاندارد یک گزارش خوب (Title, Summary, Steps to Reproduce, Impact, Remediation, PoC) را از راهنمای HackerOne یاد بگیر و یک تمپلیت شخصی در Obsidian بساز.",
  [R("HackerOne — Quality Reports (رایگان)", "https://docs.hackerone.com/en/articles/8475116-quality-reports"),
   R("Bugcrowd Vulnerability Rating Taxonomy", "https://bugcrowd.com/vulnerability-rating-taxonomy")],
  hours=2, kind="learn")

d(p9, "مطالعهٔ عمیق ۱۰ گزارش افشاشدهٔ برتر",
  "۱۰ گزارش با بالاترین امتیاز از HackerOne Hacktivity بخوان و برای هرکدام تحلیل کن: چطور باگ پیدا شد؟ چرا impact بالا بود؟ گزارش چطور نوشته شده بود؟",
  [R("HackerOne Hacktivity", "https://hackerone.com/hacktivity"),
   R("Awesome Bugbounty Writeups (رایگان)", "https://github.com/devanshbatham/Awesome-Bugbounty-Writeups")],
  hours=2, kind="learn")

d(p9, "شکار روز ۱: تست احراز هویت و کنترل دسترسی روی هدف",
  "روی برنامهٔ هدفی که در فاز ۷ انتخاب کردی، تمرکز کامل روی احراز هویت، مدیریت سشن و IDOR بگذار. هر مسیر مشکوک را در Obsidian ثبت کن حتی اگر مطمئن نیستی باگ است.",
  [R("چک‌لیست تست Authentication — PortSwigger", "https://portswigger.net/web-security/authentication")],
  hours=3, kind="practice")

d(p9, "شکار روز ۲: تست ورودی‌ها برای XSS و Injection",
  "تمام فیلدهای ورودی، پارامترهای URL، و هدرهای قابل‌کنترل هدف را برای XSS و انواع Injection با Burp Intruder فاز کن.",
  [R("PayloadsAllTheThings — XSS", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection")],
  hours=3, kind="practice")

d(p9, "شکار روز ۳: تست منطق کسب‌وکار (Business Logic)",
  "فرایندهای چندمرحله‌ای هدف (پرداخت، تخفیف، دعوت دوستان، ارتقای پلن) را برای باگ‌های منطقی تست کن — این‌ها را هیچ اسکنری پیدا نمی‌کند و اغلب پاداش بالایی دارند.",
  [R("PortSwigger — Business logic vulnerabilities", "https://portswigger.net/web-security/logic-flaws")],
  hours=3, kind="practice")

d(p9, "شکار روز ۴: بررسی اندپوینت‌های API و موبایل مرتبط",
  "اگر هدف اپ موبایل یا API عمومی دارد، مهارت‌های فاز ۸ را روی آن پیاده کن؛ اگر ندارد، روی سطح حمله‌ای که در Recon فاز ۷ کشف کردی عمیق‌تر شو.",
  [R("چک‌لیست API Testing — PortSwigger", "https://portswigger.net/web-security/api-testing")],
  hours=3, kind="practice")

d(p9, "نوشتن اولین گزارش کامل (حتی اگر یک VDP ساده باشد)",
  "هرچیزی که تا الان پیدا کردی — حتی یک باگ کم‌ریسک — را با فرمت حرفه‌ای که در روز اول این فاز ساختی گزارش کن. یک PoC واضح (اسکرین‌شات یا ویدیوی کوتاه) اضافه کن.",
  [R("ابزار رایگان ضبط اسکرین‌کست — ShareX/OBS Studio", "https://obsproject.com/")],
  hours=3, kind="milestone")

d(p9, "یادگیری از رد شدن گزارش (Duplicate/Not Applicable)",
  "دلایل رایج رد شدن گزارش‌ها (Duplicate, Informative, N/A, Out of Scope) را از مستندات HackerOne بخوان تا با ذهنیت درست به Triage نگاه کنی و ناامید نشوی.",
  [R("HackerOne — Report States (Duplicate/Not Applicable/Informative)", "https://docs.hackerone.com/en/articles/8475030-report-states")],
  hours=1, kind="learn")

d(p9, "شکار روز ۵: تمرکز روی یک کلاس آسیب‌پذیری تخصصی",
  "یکی از کلاس‌های کم‌رقابت‌تر (Race Condition، SSRF، یا Request Smuggling) را که در فاز ۵ یاد گرفتی، به‌طور اختصاصی روی هدف تست کن.",
  [R("PortSwigger — Race Conditions", "https://portswigger.net/web-security/race-conditions")],
  hours=3, kind="practice")

d(p9, "گسترش دامنهٔ شکار: انتخاب هدف دوم و سوم",
  "دو برنامهٔ باگ‌بانتی دیگر (ترجیحاً با تکنولوژی متفاوت از هدف اول) انتخاب کن تا سرعت Recon و تست‌ات را افزایش دهی و تنوع تجربه کسب کنی.",
  [R("HackerOne Directory", "https://hackerone.com/directory/programs")],
  hours=2, kind="practice")

d(p9, "شکار مستمر و ساخت عادت روزانه",
  "یک بلوک زمانی ثابت روزانه یا هفتگی برای شکار مستمر تعیین کن. هر یافته (باگ باشد یا نباشد) را در Obsidian با برچسب (Confirmed/Duplicate/Triaged/Rejected) ثبت کن تا آمار پیشرفتت مشخص باشد.",
  [R("Obsidian (رایگان) — برای ساخت جدول ردیابی شخصی", "https://obsidian.md/")],
  hours=3, kind="practice")

d(p9, "ساخت رزومه و پروفایل عمومی هانتر",
  "یک رزومهٔ کوتاه امنیتی و یک پروفایل GitHub با ابزارهای Recon شخصی‌ات که در طول مسیر نوشتی بساز و عمومی کن — این پورتفولیو در آینده مستقیماً روی فرصت‌های شغلی اثر می‌گذارد.",
  [R("نمونه رزومهٔ امنیتی — الهام از NahamSec Resources", "https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters")],
  hours=2, kind="review")

# ===========================================================================
# فاز ۱۰ — مباحث پیشرفته و رشد مستمر
# ===========================================================================
p10 = phase("p10", "مباحث پیشرفته و رشد مستمر", "این‌جا مسیر «تمام» نمی‌شود؛ این فاز چارچوب یادگیری مادام‌العمر توست", "♾️", "#1e293b")

d(p10, "HTTP/2 و HTTP/3 از دید امنیتی",
  "تفاوت‌های HTTP/2 با HTTP/1.1 و پیامدهای امنیتی‌اش (خصوصاً برای Request Smuggling) را از تحقیق James Kettle بخوان.",
  [R("James Kettle — HTTP/2: The Sequel is Always Worse (رایگان، PortSwigger Research)", "https://portswigger.net/research/http2")],
  hours=3, kind="learn")

d(p10, "HTTP Desync Attacks و Web Cache Poisoning — تحقیقات اصلی",
  "دو تحقیق پایه‌ای James Kettle دربارهٔ Request Smuggling و Cache Poisoning را کامل بخوان — این‌ها مرجع اصلی صنعت در این حوزه‌اند.",
  [R("HTTP Desync Attacks (رایگان)", "https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn"),
   R("Practical Web Cache Poisoning (رایگان)", "https://portswigger.net/research/practical-web-cache-poisoning")],
  hours=3, kind="learn")

d(p10, "پارسر دیفرنشیال: تحقیق Orange Tsai",
  "ارائهٔ معروف Orange Tsai دربارهٔ «Breaking Parser Logic» و نمونهٔ Nginx off-by-slash را ببین/بخوان — نمونهٔ کامل از تفکر خلاقانه در پیدا کردن باگ‌های نو.",
  [R("Orange Tsai — اسلایدهای Breaking Parser Logic (رایگان، GitHub)", "https://github.com/orangetw/My-Presentation-Slides/blob/main/data/2018-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out.pdf"),
   R("ویدیوی کامل ارائه در DEF CON 26 (رایگان)", "https://www.youtube.com/watch?v=28xWcRegncw")],
  hours=2, kind="learn")

d(p10, "Reverse Proxy و Weird Proxies",
  "تحقیق «weird_proxies» Aleksei Tiurin دربارهٔ رفتارهای غیرمنتظرهٔ پروکسی‌های معکوس را مرور کن — منبع الهام برای کشف باگ‌های سفارشی در معماری‌های پیچیده.",
  [R("weird_proxies — GitHub (رایگان)", "https://github.com/GrrrDog/weird_proxies")],
  hours=2, kind="learn")

d(p10, "OAuth 2.0 عمیق: Getting Started with OAuth 2.0",
  "مفاهیم عمیق‌تر OAuth (Authorization Code Flow, PKCE, state parameter) را مرور کن تا باگ‌های پیچیده‌تر OAuth را هم تشخیص بدهی.",
  [R("OAuth 2.0 Simplified — راهنمای آنلاین رایگان", "https://www.oauth.com/")],
  hours=2, kind="learn")

d(p10, "ساخت اپ آسیب‌پذیر شخصی با یک فریم‌ورک",
  "با Django یا Laravel (هر دو رایگان) یک اپ کوچک بساز و عمداً چند آسیب‌پذیری در آن قرار بده — ساختن یک آسیب‌پذیری، فهم عمیق‌تری از exploit کردنش به تو می‌دهد.",
  [R("Django (رایگان)", "https://www.djangoproject.com/"),
   R("Laravel (رایگان)", "https://laravel.com/")],
  hours=3, kind="practice")

d(p10, "Web LLM Attacks — عمیق‌تر",
  "لب‌های Web LLM Attacks پورت‌سویگر را که تازه معرفی شده دوباره مرور کن و مقالات جدید دربارهٔ Prompt Injection را دنبال کن — این حوزه به‌سرعت در حال رشد است.",
  [R("PortSwigger — Web LLM Attacks", "https://portswigger.net/web-security/llm-attacks")],
  hours=2, kind="learn")

d(p10, "شرکت در یک CTF واقعی",
  "در یک مسابقهٔ CTF رایگان و عمومی (از طریق CTFtime) ثبت‌نام کن و حداقل چند ساعت با یک تیم یا به‌تنهایی روی چالش‌های وب کار کن.",
  [R("CTFtime — تقویم مسابقات CTF (رایگان)", "https://ctftime.org/"),
   R("picoCTF — مسابقهٔ همیشگی رایگان", "https://picoctf.org/")],
  hours=4, kind="practice")

d(p10, "دنبال کردن اخبار روز امنیت وب",
  "یک لیست منبع خبری روزانه بساز (توییتر/ایکس محققان برتر، خبرنامه‌های رایگان مثل tl;dr sec) و آن را به یک عادت روزانهٔ ۱۵ دقیقه‌ای تبدیل کن.",
  [R("tl;dr sec — خبرنامهٔ رایگان امنیت", "https://tldrsec.com/"),
   R("PortSwigger Research Blog (رایگان)", "https://portswigger.net/research")],
  hours=1, kind="learn")

d(p10, "بازبینی و آپدیت متدولوژی شخصی نهایی",
  "کل سند Methodology در Obsidian که از روز اول ساختی را بازبینی و بازنویسی کن. این سند حالا باید یک متدولوژی شکار کاملاً شخصی‌سازی‌شده باشد که هر بار شکار می‌کنی از آن پیروی می‌کنی.",
  [R("Bug Bounty Roadmap Voorivex — برای الهام نهایی", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")],
  hours=2, kind="review")

d(p10, "جمع‌بندی نهایی نقشه‌راه و برنامهٔ ۶ ماه آینده",
  "یک سند نهایی بنویس: چه چیزهایی یاد گرفتی، در کدام کلاس آسیب‌پذیری قوی‌تری، و برنامهٔ ۶ ماه بعدی‌ات (تخصص در یک حوزه، شرکت در برنامه‌های Private، یا مسیر شغلی AppSec) چیست. این نقطهٔ پایان نیست — این نقطهٔ شروع شکار حرفه‌ای توست.",
  [R("لیست کامل NahamSec برای ادامهٔ مسیر", "https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters")],
  hours=2, kind="milestone")

# ===========================================================================
# خروجی نهایی
# ===========================================================================
out = {
    "generated_days": day_counter,
    "phases": phases,
}

os.makedirs("data", exist_ok=True)
with open("data/roadmap.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"OK: {len(phases)} phases, {day_counter} days written to data/roadmap.json")
