#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transforms the Persian index.html into en/index.html: swaps UI copy, paths, digit
formatting and direction, while reusing the exact same CSS/logic architecture."""
import re

SRC = "index.html"
DST = "en/index.html"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

REPLACEMENTS = [
    # <html> tag
    ('<html lang="fa" dir="rtl">', '<html lang="en" dir="ltr">'),
    # head
    ('<title>نقشه‌راه کامل باگ‌بانتی | از صفر تا حرفه‌ای</title>',
     '<title>Complete Bug Bounty Roadmap | Zero to Professional</title>'),
    ('<meta name="description" content="نقشه‌راه روز به روز، رایگان ۱۰۰٪ و فارسی برای یادگیری باگ‌بانتی از صفر تا حرفه‌ای — بر پایهٔ Voorivex، یاشار شاهین‌زاده، PortSwigger Academy، Hacker101 و منابع معتبر جهانی.">',
     '<meta name="description" content="A day-by-day, 100% free roadmap for learning bug bounty hunting from zero to professional — built on Voorivex, Yashar Shahinzadeh, PortSwigger Academy, Hacker101, and the world\'s best free resources.">'),
    # asset paths (must run before generic 'assets/' collisions — order matters, do longer paths first)
    ('href="assets/logo.svg"', 'href="../assets/logo.svg"'),
    ('href="assets/favicon-32.png"', 'href="../assets/favicon-32.png"'),
    ('href="assets/apple-touch-icon.png"', 'href="../assets/apple-touch-icon.png"'),
    ('<a href="./" class="brand"><img src="assets/logo.svg" alt="logo" class="brand-logo"><span>Bug Bounty Roadmap</span></a>',
     '<a href="./" class="brand"><img src="../assets/logo.svg" alt="logo" class="brand-logo"><span>Bug Bounty Roadmap</span></a>'),
    # font stack: add Inter for a cleaner english sans body, keep Share Tech Mono / JetBrains for headings
    ("font-family:'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;",
     "font-family:'Inter','Segoe UI',system-ui,sans-serif;"),
    ("family=Vazirmatn:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Share+Tech+Mono&display=swap",
     "family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Share+Tech+Mono&display=swap"),
    # hero h1 gets terminal font for hacker feel
    (".hero h1{\n    font-size:clamp(2rem, 5vw, 3.3rem);\n    font-weight:900;margin:0 0 16px;\n    letter-spacing:-.02em;",
     ".hero h1{\n    font-family:'Share Tech Mono', monospace;\n    font-size:clamp(1.7rem, 4.6vw, 3rem);\n    font-weight:400;margin:0 0 16px;\n    letter-spacing:-.01em;"),
    # topbar / notif
    ('title="تازه‌ها"', 'title="Updates"'),
    # hero
    ('<span class="kicker">🐞 نقشه‌راه غیررسمی و متن‌باز جامعهٔ فارسی‌زبان</span>',
     '<span class="kicker">🐞 an unofficial, open-source community roadmap</span>'),
    ('<h1><span class="type-cursor">نقشه‌راه کامل باگ‌بانتی</span><br>از صفر تا حرفه‌ای</h1>',
     '<h1><span class="type-cursor">Complete Bug Bounty Roadmap</span><br>Zero to Professional</h1>'),
    ("""    <p class="lead">
      یک برنامهٔ روز‌به‌روز، دقیق و کاملاً رایگان برای کسی که هیچ پیش‌زمینه‌ای ندارد و می‌خواهد
      به یک باگ‌بانتی‌هانتر حرفه‌ای تبدیل شود — برگرفته از آموزش‌های
      <b>یاشار شاهین‌زاده</b> و <b>Voorivex</b>، آکادمی <b>PortSwigger</b>،
      <b>Hacker101</b> و بهترین منابع رایگان جهانی. هیچ‌جای این نقشه‌راه پولی نیست.
    </p>""",
     """    <p class="lead">
      A precise, day-by-day, completely free program for a complete beginner who wants to
      become a professional bug bounty hunter — built from the free teachings of
      <b>Yashar Shahinzadeh</b> and <b>Voorivex</b>, <b>PortSwigger</b> Academy,
      <b>Hacker101</b>, and the best free resources in the world. Nothing here is paywalled.
    </p>"""),
    ("""      <span class="pill">💯 <b>۱۰۰٪ رایگان</b></span>
      <span class="pill">🇮🇷 <b>محتوای فارسی + جهانی</b></span>
      <span class="pill">📅 <b id="stat-days-badge">—</b> روز برنامه‌ریزی‌شده</span>
      <span class="pill">✅ ردیابی پیشرفت در همین صفحه</span>""",
     """      <span class="pill">💯 <b>100% Free</b></span>
      <span class="pill">🌐 <b>Global free resources</b></span>
      <span class="pill">📅 <b id="stat-days-badge">—</b> days planned</span>
      <span class="pill">✅ Progress tracking on this page</span>"""),
    ('<h3>🔗 منابع اصلی این نقشه‌راه</h3>', '<h3>🔗 Primary sources of this roadmap</h3>'),
    ('<a href="https://www.youtube.com/@Voorivex" target="_blank" rel="noopener">کانال یوتیوب Voorivex</a>',
     '<a href="https://www.youtube.com/@Voorivex" target="_blank" rel="noopener">Voorivex YouTube channel</a>'),
    ('<a href="https://www.youtube.com/watch?v=_UxO2qKvCEQ" target="_blank" rel="noopener">ویدیوی نقشه‌راه یاشار شاهین‌زاده</a>',
     '<a href="https://www.youtube.com/watch?v=_UxO2qKvCEQ" target="_blank" rel="noopener">Yashar Shahinzadeh\'s roadmap video</a>'),
    ('<a href="https://memoryleaks.ir/how-to-become-a-hacker/" target="_blank" rel="noopener">وبلاگ memoryleaks.ir</a>',
     '<a href="https://memoryleaks.ir/how-to-become-a-hacker/" target="_blank" rel="noopener">memoryleaks.ir blog</a>'),
    ('<a href="https://x.com/yshahinzadeh" target="_blank" rel="noopener">ایکس یاشار شاهین‌زاده</a>',
     '<a href="https://x.com/yshahinzadeh" target="_blank" rel="noopener">Yashar Shahinzadeh on X</a>'),
    ('<a href="https://blog.voorivex.team/bug-bounty-roadmap-from-scratch" target="_blank" rel="noopener">بلاگ Voorivex Team</a>',
     '<a href="https://blog.voorivex.team/bug-bounty-roadmap-from-scratch" target="_blank" rel="noopener">Voorivex Team blog</a>'),
    ('<a href="https://voorivex.academy/" target="_blank" rel="noopener">آکادمی Voorivex</a>',
     '<a href="https://voorivex.academy/" target="_blank" rel="noopener">Voorivex Academy</a>'),
    ('<a href="https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters" target="_blank" rel="noopener">NahamSec Resources</a>',
     '<a href="https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters" target="_blank" rel="noopener">NahamSec Resources</a>'),
    # how-to-use section
    ('<h3>🧭 چطور از این نقشه‌راه استفاده کنم؟</h3>', '<h3>🧭 How do I use this roadmap?</h3>'),
    ("""      <div>• <b style="color:var(--text)">پیوسته پیش نرو، ولی پیوسته بمان:</b> اگر یک «روز» بیشتر از یک روز واقعی طول کشید عیبی ندارد — ترتیب مهم‌تر از سرعت است. عقب افتادن از برنامه شکست نیست.</div>
      <div>• <b style="color:var(--text)">رنگ‌بندی نوع روزها:</b> <span class="kind-tag kind-learn" style="margin-inline-end:4px">آموزش</span>مفهومی جدید،
        <span class="kind-tag kind-practice" style="margin-inline-end:4px">تمرین عملی</span>دست‌به‌کیبورد شو،
        <span class="kind-tag kind-review" style="margin-inline-end:4px">مرور</span>جمع‌بندی بدون منبع جدید،
        <span class="kind-tag kind-milestone">نقطهٔ عطف</span>چک‌پوینت بزرگ برای سنجش پیشرفت واقعی‌ات.</div>
      <div>• <b style="color:var(--text)">مستندسازی مهم‌تر از سرعت است:</b> در تمام مسیر، یک Vault در Obsidian یا Notion کنار خودت نگه دار و هر نکته را یادداشت کن؛ این عادت مهم‌ترین دارایی یک هانتر حرفه‌ای است.</div>
      <div>• <b style="color:var(--text)">همیشه قانونی بمان:</b> فقط در محدودهٔ Scope مجاز برنامه‌های باگ‌بانتی، VDP ها، یا محیط‌های آموزشی طراحی‌شده برای هک (مثل PortSwigger Academy، Hacker101، DVWA) تمرین کن.</div>""",
     """      <div>• <b style="color:var(--text)">Keep moving, don't rush:</b> it's fine if a "day" takes longer than one real day — order matters more than speed. Falling behind schedule is not failure.</div>
      <div>• <b style="color:var(--text)">Day-type color coding:</b> <span class="kind-tag kind-learn" style="margin-inline-end:4px">Learn</span>a new concept,
        <span class="kind-tag kind-practice" style="margin-inline-end:4px">Hands-on</span>get your hands on the keyboard,
        <span class="kind-tag kind-review" style="margin-inline-end:4px">Review</span>consolidate, no new resource,
        <span class="kind-tag kind-milestone">Milestone</span>a big checkpoint to gauge real progress.</div>
      <div>• <b style="color:var(--text)">Documentation beats speed:</b> keep an Obsidian or Notion vault next to you the whole way and log every insight — this habit is a professional hunter's single most valuable asset.</div>
      <div>• <b style="color:var(--text)">Always stay legal:</b> only practice within the authorized scope of bug bounty programs, VDPs, or purpose-built training environments (PortSwigger Academy, Hacker101, DVWA).</div>"""),
    # heatmap section
    ('<h3 style="margin:0;">📊 نمودار فعالیت من</h3>', '<h3 style="margin:0;">📊 My Activity Graph</h3>'),
    ("""      <span>کم</span>
      <span class="hm-cell" data-level="0"></span>
      <span class="hm-cell" data-level="1"></span>
      <span class="hm-cell" data-level="2"></span>
      <span class="hm-cell" data-level="3"></span>
      <span class="hm-cell" data-level="4"></span>
      <span>زیاد</span>
      <span style="margin-inline-start:auto; color:var(--text-faint);">داده فقط در همین مرورگر ذخیره می‌شود</span>""",
     """      <span>Less</span>
      <span class="hm-cell" data-level="0"></span>
      <span class="hm-cell" data-level="1"></span>
      <span class="hm-cell" data-level="2"></span>
      <span class="hm-cell" data-level="3"></span>
      <span class="hm-cell" data-level="4"></span>
      <span>More</span>
      <span style="margin-inline-start:auto; color:var(--text-faint);">Data is stored only in this browser</span>"""),
    ('direction:rtl; width:max-content;', 'direction:ltr; width:max-content;'),
    # controls
    ('placeholder="🔍 جست‌وجو در عنوان، توضیح یا منابع روزها...">',
     'placeholder="🔍 Search titles, descriptions, or resources...">'),
    ('<button class="filter-btn active" data-filter="all">همه</button>',
     '<button class="filter-btn active" data-filter="all">All</button>'),
    ('<button class="filter-btn" data-filter="todo">باقی‌مانده</button>',
     '<button class="filter-btn" data-filter="todo">Remaining</button>'),
    ('<button class="filter-btn" data-filter="done">انجام‌شده</button>',
     '<button class="filter-btn" data-filter="done">Done</button>'),
    ('<span class="progress-pct" id="overall-pct">۰٪</span>', '<span class="progress-pct" id="overall-pct">0%</span>'),
    # footer
    ('<span>ساخته‌شده با هوش مصنوعی <a href="https://claude.com/claude-code" target="_blank" rel="noopener">Claude Code</a> بر پایهٔ تحقیق روی منابع معتبر آموزش امنیت</span>',
     '<span>Built with <a href="https://claude.com/claude-code" target="_blank" rel="noopener">Claude Code</a>, based on research into reputable security-education resources</span>'),
    ('<a href="https://github.com/hack3rrabbit/bug-bounty-roadmap" target="_blank" rel="noopener">کد منبع در گیت‌هاب</a>',
     '<a href="https://github.com/hack3rrabbit/bug-bounty-roadmap" target="_blank" rel="noopener">Source code on GitHub</a>'),
    ('<span>پیشرفت شما فقط در مرورگر همین دستگاه (localStorage) ذخیره می‌شود</span>',
     '<span>Your progress is stored only in this browser (localStorage)</span>'),
    ('<button class="reset-btn" id="reset-progress">پاک کردن پیشرفت</button>',
     '<button class="reset-btn" id="reset-progress">Reset progress</button>'),
    ('<div>این یک پروژهٔ غیررسمی و جامعه‌محور است؛ هیچ‌گونه ارتباط رسمی با Voorivex یا یاشار شاهین‌زاده ندارد — صرفاً برای گردآوری بهترین منابع رایگان ساخته شده است.</div>',
     '<div>This is an unofficial, community-built project with no official affiliation to Voorivex or Yashar Shahinzadeh — built purely to curate the best free resources. <a href="../">فارسی</a></div>'),
    ('<button class="top-btn" id="top-btn" title="برو بالا">↑</button>',
     '<button class="top-btn" id="top-btn" title="Back to top">↑</button>'),
    # ---------------- JS ----------------
    ("const KIND_LABEL = { learn:'آموزش', practice:'تمرین عملی', review:'مرور', milestone:'نقطهٔ عطف' };",
     "const KIND_LABEL = { learn:'Learn', practice:'Hands-on', review:'Review', milestone:'Milestone' };"),
    ("document.getElementById('stat-days-badge').textContent = totalDays.toLocaleString('fa-IR');",
     "document.getElementById('stat-days-badge').textContent = totalDays.toLocaleString('en-US');"),
    ("""  const items = [
    [totalDays, 'روز آموزشی'],
    [ROADMAP.phases.length, 'فاز اصلی'],
    [totalResources, 'منبع رایگان یکتا'],
    [Math.round(totalHours), 'ساعت محتوا'],
    [Math.round(totalDays/6*7/30*10)/10, 'ماه تقویمی (با ۶ روز مطالعه/هفته)'],
  ];
  statsEl.innerHTML = items.map(([n,l])=>`<div class="stat"><div class="num">${(''+n).replace(/[0-9]/g,x=>'۰۱۲۳۴۵۶۷۸۹'[x])}</div><div class="lbl">${l}</div></div>`).join('');""",
     """  const items = [
    [totalDays, 'training days'],
    [ROADMAP.phases.length, 'main phases'],
    [totalResources, 'unique free resources'],
    [Math.round(totalHours), 'hours of content'],
    [Math.round(totalDays/6*7/30*10)/10, 'calendar months (6 study days/wk)'],
  ];
  statsEl.innerHTML = items.map(([n,l])=>`<div class="stat"><div class="num">${n}</div><div class="lbl">${l}</div></div>`).join('');"""),
    ("function faNum(n){ return String(n).replace(/[0-9]/g, x=>'۰۱۲۳۴۵۶۷۸۹'[x]); }",
     "function faNum(n){ return String(n); } // no digit localization needed in English"),
    ('<span class="day-num">روز ${faNum(day.day)}</span>', '<span class="day-num">Day ${faNum(day.day)}</span>'),
    ("<span class=\"hours\">⏱ ${faNum(day.hours)} ساعت تخمینی</span>",
     "<span class=\"hours\">⏱ ${faNum(day.hours)}h estimated</span>"),
    ("""        <input type="checkbox" ${isDone?'checked':''} onchange="toggleDay(${day.day}, this.checked)">
        انجام شد""",
     """        <input type="checkbox" ${isDone?'checked':''} onchange="toggleDay(${day.day}, this.checked)">
        Done"""),
    ('<button type="button" onclick="toggleTimeForm(${day.day})">⏱ ثبت زمان مطالعه</button>',
     '<button type="button" onclick="toggleTimeForm(${day.day})">⏱ Log study time</button>'),
    ("${loggedMin>0 ? '('+faNum(Math.round(loggedMin/60*10)/10)+' ساعت ثبت‌شده)' : ''}",
     "${loggedMin>0 ? '('+faNum(Math.round(loggedMin/60*10)/10)+'h logged)' : ''}"),
    ('<input type="number" min="1" max="600" placeholder="دقیقه" id="tf-input-${day.day}">',
     '<input type="number" min="1" max="600" placeholder="minutes" id="tf-input-${day.day}">'),
    ('<button type="button" onclick="submitTimeLog(${day.day})">ثبت</button>',
     '<button type="button" onclick="submitTimeLog(${day.day})">Save</button>'),
    ("<div class=\"empty-state hidden\" id=\"empty-state\">چیزی با این فیلتر/جست‌وجو پیدا نشد 🕵️</div>",
     "<div class=\"empty-state hidden\" id=\"empty-state\">Nothing matches this filter/search 🕵️</div>"),
    ("${faNum(doneCount)}/${faNum(p.days.length)} روز`;", "${faNum(doneCount)}/${faNum(p.days.length)} days`;"),
    ("<span class=\"phase-count\">${faNum(doneCount)}/${faNum(p.days.length)} روز</span>",
     "<span class=\"phase-count\">${faNum(doneCount)}/${faNum(p.days.length)} days</span>"),
    ("document.getElementById('overall-pct').textContent = faNum(pct)+'٪ ('+faNum(done)+'/'+faNum(days.length)+')';",
     "document.getElementById('overall-pct').textContent = faNum(pct)+'% ('+faNum(done)+'/'+faNum(days.length)+')';"),
    ("  // اولین‌بار که یک روز تیک می‌خورد، ساعت تخمینی‌اش خودکار به لاگ زمان امروز اضافه می‌شود\n",
     "  // The first time a day is checked, its estimated hours are auto-logged to today\n"),
    ("if(badge) badge.textContent = '('+faNum(Math.round(dayTime[dayNum]/60*10)/10)+' ساعت ثبت‌شده)';",
     "if(badge) badge.textContent = '('+faNum(Math.round(dayTime[dayNum]/60*10)/10)+'h logged)';"),
    ('title="${key} — ${mins>0? Math.round(mins/60*10)/10+\' ساعت\':\'بدون فعالیت\'}"',
     'title="${key} — ${mins>0? Math.round(mins/60*10)/10+\' hours\':\'no activity\'}"'),
    ("summary.textContent = `${faNum(activeDays)} روز فعال · ${faNum(Math.round(totalMinutes/60*10)/10)} ساعت ثبت‌شده در ${faNum(WEEKS)} هفتهٔ اخیر`;",
     "summary.textContent = `${faNum(activeDays)} active days · ${faNum(Math.round(totalMinutes/60*10)/10)}h logged in the last ${faNum(WEEKS)} weeks`;"),
    ("""    if(confirm('مطمئنی می‌خوای کل پیشرفتت پاک بشه؟ این کار قابل بازگشت نیست.')){""",
     """    if(confirm('Are you sure you want to clear all your progress? This cannot be undone.')){"""),
    ("document.getElementById('lang-toggle').addEventListener('click', ()=>{ window.location.href = 'en/'; });",
     "document.getElementById('lang-toggle').addEventListener('click', ()=>{ window.location.href = '../'; });"),
    ('title="English version">EN', 'title="نسخهٔ فارسی">FA'),
    # notifications: use English fields + fix panel content, fetch changelog from ../data
    ("""    panel.innerHTML = items.map(it=>`
      <div class="notif-item">
        <div class="nt-date">${it.date}</div>
        <div class="nt-title">${it.title_fa}</div>
        <div class="nt-body">${it.body_fa}</div>
      </div>`).join('');""",
     """    panel.innerHTML = items.map(it=>`
      <div class="notif-item">
        <div class="nt-date">${it.date}</div>
        <div class="nt-title">${it.title_en}</div>
        <div class="nt-body">${it.body_en}</div>
      </div>`).join('');"""),
    ("fetch('data/changelog.json')", "fetch('../data/changelog.json')"),
    ("fetch('data/roadmap.json')", "fetch('../data/roadmap.en.json')"),
    ("document.getElementById('content').innerHTML = '<p style=\"text-align:center;color:var(--red)\">خطا در بارگذاری داده‌های نقشه‌راه. لطفاً صفحه را رفرش کنید.</p>';",
     "document.getElementById('content').innerHTML = '<p style=\"text-align:center;color:var(--red)\">Failed to load roadmap data. Please refresh the page.</p>';"),
]

missing = []
for old, new in REPLACEMENTS:
    if old not in html:
        missing.append(old[:80])
    html = html.replace(old, new)

if missing:
    print(f"WARNING: {len(missing)} replacement(s) not found in source:")
    for m in missing:
        print("  -", m)
else:
    print(f"All {len(REPLACEMENTS)} replacements applied cleanly.")

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote {DST}")
