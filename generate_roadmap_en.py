#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English content generator — mirrors generate_roadmap.py structurally (same phase IDs,
same day counts per phase via the same COMPACTION_TARGETS) so day N means the same
thing in both languages. Output: data/roadmap.en.json
"""
import json, os

phases = []

def phase(pid, title, subtitle, icon, color):
    p = {"id": pid, "title": title, "subtitle": subtitle, "icon": icon, "color": color, "days": []}
    phases.append(p)
    return p

def d(p, title, task, resources, hours=2, kind="learn"):
    p["days"].append({"title": title, "task": task, "resources": resources, "hours": hours, "kind": kind})

def R(t, u):
    return {"t": t, "u": u}

KIND_PRIORITY = ["milestone", "practice", "learn", "review"]

def compact(days, target):
    n = len(days)
    if n <= target:
        return days
    groups = [[] for _ in range(target)]
    for idx, day in enumerate(days):
        groups[idx * target // n].append(day)
    merged = []
    for g in groups:
        if len(g) == 1:
            merged.append(g[0]); continue
        title = " + ".join(x["title"] for x in g)
        task = " ".join(f"({i+1}) {x['task']}" for i, x in enumerate(g))
        resources, seen = [], set()
        for x in g:
            for r in x["resources"]:
                if r["u"] not in seen:
                    resources.append(r); seen.add(r["u"])
        hours = round(sum(x["hours"] for x in g), 1)
        kind = next((k for k in KIND_PRIORITY if any(x["kind"] == k for x in g)), g[0]["kind"])
        merged.append({"title": title, "task": task, "resources": resources, "hours": hours, "kind": kind})
    return merged

# ===========================================================================
p0 = phase("p0", "Getting Started: Mindset & Environment", "Before your first command, know why you're doing this and what you're doing it with", "🚀", "#7c3aed")

d(p0, "Why bug bounty? The real path into this career",
  "Read Yashar Shahinzadeh's full post 'How to Become a Hacker'. Start a Notion/Obsidian vault and write down your real motivation for this path — you'll revisit and update this document throughout the whole roadmap.",
  [R("Yashar Shahinzadeh's blog — How to Become a Hacker", "https://memoryleaks.ir/how-to-become-a-hacker/"),
   R("Voorivex Team — Bug Bounty Roadmap from Scratch", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")], hours=2, kind="learn")
d(p0, "Watch Yashar Shahinzadeh's roadmap video",
  "Watch the full roadmap video and take notes. Turn every recommendation into a checklist item in your personal doc.",
  [R("Roadmap video — Yashar Shahinzadeh (Voorivex YouTube)", "https://www.youtube.com/watch?v=_UxO2qKvCEQ"),
   R("Voorivex YouTube channel", "https://www.youtube.com/@Voorivex")], hours=1, kind="learn")
d(p0, "Set up a Linux VM and hacking environment",
  "Install VirtualBox/VMware and spin up Kali Linux or Parrot OS in a VM. Take an initial snapshot so you can always roll back a broken environment.",
  [R("Download Kali Linux", "https://www.kali.org/get-kali/"), R("VirtualBox (free)", "https://www.virtualbox.org/"),
   R("Kali in VirtualBox install guide", "https://www.kali.org/docs/virtualization/install-virtualbox-guest-vm/")], hours=2, kind="practice")
d(p0, "Create profiles on bug bounty platforms",
  "Sign up on HackerOne and Bugcrowd, browse Hacktivity on both to see the format of public reports and what gets accepted. Read at least 5 real disclosed reports end to end.",
  [R("HackerOne Hacktivity", "https://hackerone.com/hacktivity"), R("Bugcrowd Crowdstream", "https://bugcrowd.com/crowdstream"),
   R("Awesome Bugbounty Writeups", "https://github.com/devanshbatham/Awesome-Bugbounty-Writeups")], hours=2, kind="practice")
d(p0, "Documentation tooling and your personal methodology",
  "Build an Obsidian (or Notion) vault with folders: Methodology, CVE/Writeups, Targets, Reports. Start logging everything you learn from today — this habit is the single most valuable asset of a professional hunter.",
  [R("Obsidian (free)", "https://obsidian.md/"), R("Voorivex — building a personal methodology", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")], hours=1, kind="learn")

# ===========================================================================
p1 = phase("p1", "Linux & the Command Line", "Without terminal fluency you can't run any hacking tool correctly", "🐧", "#059669")
d(p1, "Linux basics: filesystem and core commands",
  "Practice the 'Linux Basics' chapter: ls, cd, pwd, cat, cp, mv, rm, mkdir, man. Use man/--help instead of Google for every command.",
  [R("Linux Journey — Grasshopper", "https://linuxjourney.com/lesson/the-shell"), R("TryHackMe — Linux Fundamentals Part 1 (free)", "https://tryhackme.com/room/linuxfundamentalspart1")], hours=2, kind="learn")
d(p1, "OverTheWire Bandit — levels 0-2",
  "SSH into the Bandit server (level0/level0, password: bandit0) and solve the first three levels. Learn to find hidden files, oddly named files, and command output.",
  [R("OverTheWire Bandit", "https://overthewire.org/wargames/bandit/"), R("Bandit Level 0", "https://overthewire.org/wargames/bandit/bandit0.html")], hours=2, kind="practice")
d(p1, "Bandit — levels 3-6",
  "Practice hidden files, recursive search with find, and filtering by type/size/permission. Combine find and grep.",
  [R("Bandit Level 3", "https://overthewire.org/wargames/bandit/bandit3.html")], hours=2, kind="practice")
d(p1, "Bandit — levels 7-10",
  "Practice advanced grep, archive handling (tar/gzip/bzip2), and Base64/binary files.",
  [R("Bandit Level 7", "https://overthewire.org/wargames/bandit/bandit7.html")], hours=2, kind="practice")
d(p1, "Permissions, ownership and environment variables",
  "Learn rwx, numeric/symbolic chmod, chown, and environment variables (PATH, env), then solve Bandit levels 11-14.",
  [R("Bandit Level 11", "https://overthewire.org/wargames/bandit/bandit11.html")], hours=2, kind="practice")
d(p1, "SSH keys, ports and processes",
  "Generate an SSH key with ssh-keygen, connect with a private key, inspect running processes (ps, netstat/ss). Solve Bandit levels 15-18.",
  [R("Bandit Level 15", "https://overthewire.org/wargames/bandit/bandit15.html")], hours=2, kind="practice")
d(p1, "Cron jobs, setuid, and simple scripting",
  "Understand cron, setuid binaries, and how a binary can run as a different user. Solve Bandit levels 19-23.",
  [R("Bandit Level 19", "https://overthewire.org/wargames/bandit/bandit19.html")], hours=2, kind="practice")
d(p1, "Netcat and basic network communication",
  "Practice nc: opening a listening port, sending/receiving data, simulating a simple client-server. Solve Bandit levels 24-27.",
  [R("Bandit Level 24", "https://overthewire.org/wargames/bandit/bandit24.html"), R("Netcat guide", "https://linuxjourney.com/lesson/netcat-nc-command")], hours=2, kind="practice")
d(p1, "Git from a security angle + unusual binaries",
  "Learn Git history, exposed .git/ repos, and recovering data from old commits — directly useful for finding exposed .git/ in bug bounty. Solve Bandit levels 28-31.",
  [R("Bandit Level 28", "https://overthewire.org/wargames/bandit/bandit28.html")], hours=2, kind="practice")
d(p1, "Bandit — levels 32-33 + wrap-up",
  "Finish the remaining Bandit levels. Write a summary page in Obsidian: which Linux commands you learned and when you'd use them.",
  [R("Bandit Level 32", "https://overthewire.org/wargames/bandit/bandit32.html")], hours=2, kind="review")
d(p1, "Bash scripting basics",
  "Practice variables, loops (for/while), conditionals (if) and arguments. Write three small scripts: count files, ping a list of IPs, parse a text file.",
  [R("Bash Scripting — free GitHub guide", "https://github.com/Idnan/bash-guide"), R("Learn Shell — interactive & free", "https://www.learnshell.org/")], hours=3, kind="learn")
d(p1, "Bash scripting — advanced automation",
  "Learn arrays, functions, and pipelines (|, xargs, tee). Write a script that reads a domain list and curls each one, printing HTTP status codes — the seed of your future recon scripts.",
  [R("explainshell.com — interactive command breakdowns (free)", "https://explainshell.com/")], hours=3, kind="practice")
d(p1, "TryHackMe: Linux Fundamentals 2 and 3 (free)",
  "Finish the next two Linux Fundamentals rooms: package management (apt), services (systemctl), and a text editor (nano/vim).",
  [R("Linux Fundamentals Part 2", "https://tryhackme.com/room/linuxfundamentalspart2"), R("Linux Fundamentals Part 3", "https://tryhackme.com/room/linuxfundamentalspart3")], hours=3, kind="practice")
d(p1, "Review and self-test: Linux",
  "Without notes, write down 10 important Linux commands from memory and explain their use. Revisit any topic you get stuck on.",
  [R("Linux Journey — full review", "https://linuxjourney.com/")], hours=1, kind="review")

# ===========================================================================
p2 = phase("p2", "Networking & the HTTP Protocol", "The web runs on HTTP; if you don't understand HTTP, you can't understand any web vulnerability", "🌐", "#2563eb")
d(p2, "OSI and TCP/IP models",
  "Learn the OSI/TCP-IP layers, TCP vs UDP, and the concept of a port. Write the 7 OSI layers from memory in Obsidian.",
  [R("TryHackMe — Pre Security Path (free)", "https://tryhackme.com/path/outline/presecurity")], hours=2, kind="learn")
d(p2, "DNS from scratch",
  "Learn how DNS works, record types (A, AAAA, CNAME, MX, TXT, NS), and dig/nslookup — test them on real domains.",
  [R("Cloudflare — What is DNS (free)", "https://www.cloudflare.com/learning/dns/what-is-dns/"), R("TryHackMe — DNS in Detail", "https://tryhackme.com/room/dnsindetail")], hours=2, kind="learn")
d(p2, "HTTP from scratch — methods and status codes",
  "Read MDN in full on GET/POST/PUT/DELETE/PATCH/OPTIONS/HEAD, request/response structure, and status codes (2xx-5xx).",
  [R("MDN — HTTP Overview (free)", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"), R("MDN — HTTP Status Codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status")], hours=2, kind="learn")
d(p2, "HTTP headers and cookies",
  "Learn the important security headers (Cookie, Set-Cookie, Authorization, Content-Type, Host, Referer, Origin, CSP, HSTS). Open a real site with Burp or DevTools and identify every header of one request.",
  [R("MDN — HTTP Headers", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers"), R("MDN — HTTP Cookies", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies")], hours=2, kind="learn")
d(p2, "Install and set up Burp Suite Community",
  "Install Burp Suite Community (free), point your browser's proxy at it, install its CA certificate, and intercept your first HTTPS traffic.",
  [R("Download Burp Suite Community (free)", "https://portswigger.net/burp/communitydownload"), R("PortSwigger — setting up Burp with Firefox", "https://portswigger.net/burp/documentation/desktop/getting-started")], hours=2, kind="practice")
d(p2, "Hands-on Burp Suite: Proxy and Repeater",
  "Practice the Proxy and Repeater tabs against a test site (e.g. PortSwigger labs): intercept a request, send to Repeater, modify parameters, resend.",
  [R("PortSwigger Academy — Burp Suite Essentials", "https://portswigger.net/web-security/learning-path")], hours=2, kind="practice")
d(p2, "HTTPS/TLS in plain terms",
  "Understand the TLS handshake, digital certificates, and why HTTPS blocks naive interception (conceptual level, not the math).",
  [R("Cloudflare — What is TLS (free)", "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/")], hours=1, kind="learn")
d(p2, "REST APIs and JSON",
  "Learn APIs, REST, and JSON. Use Burp against a free public API (e.g. JSONPlaceholder) and rebuild GET/POST requests in Repeater.",
  [R("JSONPlaceholder — free test API", "https://jsonplaceholder.typicode.com/"), R("MDN — Working with JSON", "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON")], hours=2, kind="practice")
d(p2, "Web servers: Apache and Nginx",
  "Learn the difference between Apache and Nginx, virtual hosts, reverse proxies, and basic config files — essential later for SSRF and request smuggling.",
  [R("DigitalOcean — free Apache vs Nginx comparison", "https://www.digitalocean.com/community/tutorials/apache-vs-nginx-practical-considerations"), R("Nginx — official docs (free)", "https://nginx.org/en/docs/")], hours=2, kind="learn")
d(p2, "Wireshark and network traffic analysis",
  "Install Wireshark and capture your own browser traffic. Find and inspect HTTP and DNS packets in it.",
  [R("Download Wireshark (free)", "https://www.wireshark.org/download.html"), R("TryHackMe — Wireshark: The Basics", "https://tryhackme.com/room/wiresharkthebasics")], hours=2, kind="practice")
d(p2, "Nmap: port and service scanning",
  "Practice a basic nmap scan (-sV, -sC, -p-) against a legal target (e.g. scanme.nmap.org) and interpret the output.",
  [R("Nmap — official reference guide (free)", "https://nmap.org/book/man.html")], hours=2, kind="practice")
d(p2, "TryHackMe: Web Fundamentals — How the Web Works",
  "Finish the starter room of the Web Fundamentals path: browsers, servers, and the full lifecycle of a web request, from a security lens.",
  [R("TryHackMe — How Websites Work (free)", "https://tryhackme.com/room/howwebsiteswork")], hours=2, kind="practice")
d(p2, "Mini project: map a full HTTP request",
  "Draw a diagram (paper or Excalidraw) of the full path from a user's click to the response rendering: DNS → TCP handshake → TLS → HTTP request → server → response → browser render.",
  [R("Excalidraw (free, online)", "https://excalidraw.com/")], hours=2, kind="review")

# ===========================================================================
p3 = phase("p3", "Programming for Hackers", "Python for scripting/automation, JavaScript for understanding and exploiting the client side", "🐍", "#d97706")
d(p3, "Python: variables, data types, conditionals",
  "Read chapters 1-3 of the free book Automate the Boring Stuff and code the exercises.",
  [R("Automate the Boring Stuff with Python (free full book)", "https://automatetheboringstuff.com/"), R("Python for Everybody — py4e (free)", "https://www.py4e.com/")], hours=3, kind="learn")
d(p3, "Python: loops and functions",
  "Practice for/while loops and writing functions. Build a script that reads a word list and performs a simple operation on each (e.g. building input permutations).",
  [R("Automate the Boring Stuff — functions chapter", "https://automatetheboringstuff.com/2e/chapter3/")], hours=3, kind="practice")
d(p3, "Python: lists, dictionaries, and file I/O",
  "Learn lists, dicts, and reading/writing text files. Write a script that reads a wordlist from a file and removes duplicate lines.",
  [R("Automate the Boring Stuff — files chapter", "https://automatetheboringstuff.com/2e/chapter9/")], hours=3, kind="practice")
d(p3, "Python: the requests library",
  "Send a GET and a POST to a real API with requests, set custom headers/cookies, and parse the JSON response.",
  [R("requests docs (free)", "https://requests.readthedocs.io/en/latest/user/quickstart/")], hours=3, kind="practice")
d(p3, "Python project: simple subdomain scanner",
  "Using requests and a small wordlist, write a script that checks a handful of common subdomains (www, api, dev, staging) on a test domain and prints each one's HTTP status.",
  [R("SecLists — ready-made recon wordlists (free)", "https://github.com/danielmiessler/SecLists")], hours=3, kind="practice")
d(p3, "Python project: broken/open link checker",
  "Extend the previous script to run concurrently (threading or concurrent.futures) for speed — the foundation of your future recon tools.",
  [R("Python concurrent.futures — official docs", "https://docs.python.org/3/library/concurrent.futures.html")], hours=3, kind="practice")
d(p3, "JavaScript: language basics",
  "Learn variables (let/const), functions, conditionals, and loops — all client-side web logic is written in this language.",
  [R("javascript.info — first steps (free)", "https://javascript.info/first-steps")], hours=3, kind="learn")
d(p3, "JavaScript: the DOM and events",
  "Learn DOM manipulation, event listeners, and innerHTML — this is exactly where XSS understanding begins.",
  [R("javascript.info — Document (free)", "https://javascript.info/document"), R("MDN — Introduction to the DOM", "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction")], hours=3, kind="learn")
d(p3, "JavaScript: Same-Origin Policy and Fetch/AJAX",
  "Learn Origin, the Same-Origin Policy, and how fetch/XMLHttpRequest work — the direct foundation of CORS and CSRF.",
  [R("MDN — Same-origin policy", "https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy"), R("javascript.info — Fetch", "https://javascript.info/fetch")], hours=3, kind="learn")
d(p3, "SQL from scratch",
  "Learn SELECT, WHERE, JOIN, UNION, and comments in SQL with a free practice database — an absolute prerequisite for SQL injection.",
  [R("SQLBolt — interactive & free", "https://sqlbolt.com/"), R("W3Schools SQL Tutorial (free)", "https://www.w3schools.com/sql/")], hours=3, kind="learn")
d(p3, "Git and GitHub for hackers",
  "Learn clone, commit, branch, and — more importantly — how to search public commit history for leaked secrets (API keys, passwords).",
  [R("Official Git book (free)", "https://git-scm.com/book/en/v2"), R("TruffleHog — find secrets in git (free)", "https://github.com/trufflesecurity/trufflehog")], hours=2, kind="learn")
d(p3, "Phase capstone: personal recon tool v1",
  "Combine everything from this phase into the first version of your personal recon tool: take a domain, check a few common subdomains, save output to CSV. You'll keep developing this tool throughout the roadmap.",
  [R("Build your own GitHub repo for it", "https://github.com/")], hours=3, kind="milestone")
d(p3, "Programming phase review",
  "Without looking at old code, write a fresh Python script that takes a URL, checks its HTTP status, and prints the response headers. Revisit any topic you get stuck on.",
  [R("Python Docs (free)", "https://docs.python.org/3/")], hours=2, kind="review")

# ===========================================================================
p4 = phase("p4", "Web Security Fundamentals & Burp Suite", "Before hunting, master the map of vulnerabilities and your core tool", "🛠️", "#dc2626")
d(p4, "OWASP Top 10 — full list",
  "Read the full 2021 OWASP Top 10 and write a one-line explanation of each in your own words in Obsidian — this framework is the reference point for the rest of the roadmap.",
  [R("OWASP Top 10 (free, official)", "https://owasp.org/www-project-top-ten/")], hours=2, kind="learn")
d(p4, "Modern web application architecture",
  "Understand the difference between traditional server-rendered apps and SPAs (React/Vue/Angular), and the role of APIs in modern architecture — the attack surface differs for each.",
  [R("MDN — SPA glossary (free)", "https://developer.mozilla.org/en-US/docs/Glossary/SPA")], hours=2, kind="learn")
d(p4, "Burp Suite: Intruder and basic fuzzing",
  "Work through the Intruder tab against a practice target (DVWA or PortSwigger labs): Sniper, payload types, and analyzing results by response length.",
  [R("PortSwigger — Burp Intruder documentation", "https://portswigger.net/burp/documentation/desktop/tools/intruder")], hours=2, kind="practice")
d(p4, "Set up DVWA for local practice",
  "Spin up DVWA (Damn Vulnerable Web Application) on your VM with XAMPP/Docker — a fully legal local environment for practicing techniques.",
  [R("DVWA (free, GitHub)", "https://github.com/digininja/DVWA"), R("Running DVWA with Docker (free)", "https://github.com/digininja/DVWA#docker")], hours=2, kind="practice")
d(p4, "Burp Suite: Decoder, Comparer and Extensions",
  "Learn Decoder for Base64/URL-encoding, practice Comparer for diffing two responses, and install a few free extensions from the BApp Store (e.g. Logger++).",
  [R("PortSwigger BApp Store (free)", "https://portswigger.net/bappstore")], hours=2, kind="practice")
d(p4, "General web pentest methodology",
  "Learn the full cycle of a web security assessment (Recon → Mapping → Testing → Exploitation → Reporting) from Bugcrowd University's free materials.",
  [R("Bugcrowd University — free (GitHub)", "https://github.com/bugcrowd/bugcrowd_university")], hours=2, kind="learn")
d(p4, "Start Yashar Shahinzadeh's free Maktabkhooneh course",
  "Find Yashar Shahinzadeh's free 'Application Security from Scratch' course on Maktabkhooneh, enroll for free, and start watching.",
  [R("Search the course on Maktabkhooneh", "https://maktabkhooneh.org/search/?q=%D8%A7%D9%85%D9%86%DB%8C%D8%AA+%D8%A7%D9%BE%D9%84%DB%8C%DA%A9%DB%8C%D8%B4%D9%86+%D8%A7%D8%B2+%D8%B5%D9%81%D8%B1"), R("His X/Twitter for new course announcements", "https://x.com/yshahinzadeh")], hours=2, kind="learn")
d(p4, "Start PortSwigger Web Security Academy — Essential Skills",
  "Before diving into vulnerability classes, finish the Essential Skills section of PortSwigger Academy to learn how the labs and platform work.",
  [R("PortSwigger Academy — Essential Skills", "https://portswigger.net/web-security/essential-skills")], hours=2, kind="practice")
d(p4, "Sign up for Hacker101 and start the videos",
  "Sign up for Hacker101 (completely free, built by HackerOne) and watch the first introductory videos. You'll continue this alongside PortSwigger throughout the roadmap.",
  [R("Hacker101 (free)", "https://www.hacker101.com/"), R("Hacker101 — videos section", "https://www.hacker101.com/videos")], hours=2, kind="learn")
d(p4, "Review: full mind map of your progress so far",
  "Draw a mind map of everything you've learned so far: Linux, networking, programming, tools. This is your foundation before entering the vulnerabilities phase.",
  [R("XMind (free)", "https://xmind.app/")], hours=1, kind="review")

# ===========================================================================
p5 = phase("p5", "Core Web Vulnerabilities (PortSwigger Academy)", "The heart of this roadmap: theory + free PortSwigger labs for every vulnerability class", "🎯", "#be123c")

swigger_topics = [
    ("SQL Injection", "sql-injection", 18, 2, 6.0, "The king of server-side vulnerabilities; solve all 18 labs carefully, from UNION-based to time-delay blind."),
    ("Cross-Site Scripting (XSS)", "cross-site-scripting", 30, 3, 6.5, "The most common bug in bug bounty programs; work through Reflected, Stored and DOM-based across all 30 labs."),
    ("Cross-Site Request Forgery (CSRF)", "csrf", 12, 1, 5.0, "Fully understand CSRF tokens, SameSite cookies, and common bypasses."),
    ("Cross-Origin Resource Sharing (CORS)", "cors", 3, 1, 2.5, "Misconfigured CORS and data theft via a malicious origin."),
    ("Clickjacking", "clickjacking", 5, 1, 3.0, "UI-redress attacks and X-Frame-Options/CSP bypasses."),
    ("Authentication", "authentication", 14, 2, 5.5, "Login bugs, password reset flaws, 2FA bypass, and guessable credentials."),
    ("Access Control (IDOR/Privilege Escalation)", "access-control", 13, 2, 5.0, "One of the most profitable classes in bug bounty; go deep on IDOR and Broken Access Control."),
    ("Path Traversal", "file-path-traversal", 6, 1, 4.0, "Accessing files outside the web root directory."),
    ("Command Injection", "os-command-injection", 5, 1, 3.5, "Executing OS commands via user input."),
    ("Business Logic Vulnerabilities", "logic-flaws", 11, 2, 4.5, "Bugs no scanner will ever find — discovered only through slow, human thinking."),
    ("Information Disclosure", "information-disclosure", 5, 1, 3.0, "Leaking sensitive data via error messages, code comments, or backup files."),
    ("File Upload Vulnerabilities", "file-upload", 7, 1, 4.5, "Web shell upload, extension/MIME-type filter bypasses."),
    ("Race Conditions", "race-conditions", 6, 2, 3.5, "Exploiting concurrent request timing; hot, low-competition, and slow to learn."),
    ("Server-Side Request Forgery (SSRF)", "ssrf", 7, 1, 4.5, "Making the server send a request to a destination of your choosing; often the way into an internal/cloud network."),
    ("XXE Injection", "xxe", 9, 1, 5.5, "XML External Entity vulnerabilities and reading server files through them."),
    ("NoSQL Injection", "nosql-injection", 4, 1, 3.0, "Injection into NoSQL databases like MongoDB."),
    ("API Testing", "api-testing", 5, 1, 3.5, "REST API testing methodology; discovering hidden endpoints."),
    ("Web Cache Deception", "web-cache-deception", 5, 1, 3.5, "Tricking a cache into storing a private page publicly."),
    ("WebSockets", "websockets", 3, 1, 2.5, "WebSocket security and CSRF-equivalent attacks over WS."),
    ("DOM-based vulnerabilities", "dom-based", 7, 1, 4.5, "Dangerous sources and sinks in client-side JavaScript."),
    ("Insecure Deserialization", "deserialization", 10, 2, 4.5, "Exploiting deserialization of untrusted data in PHP/Java/.NET/Python."),
    ("GraphQL API Vulnerabilities", "graphql", 5, 1, 3.5, "Introspection, batching attacks, and IDOR in GraphQL."),
    ("Server-Side Template Injection (SSTI)", "server-side-template-injection", 7, 1, 4.5, "Injection into template engines (Jinja2, Twig, FreeMarker) that often escalates to RCE."),
    ("Web Cache Poisoning", "web-cache-poisoning", 13, 2, 4.5, "Poisoning a cache to deliver malicious content to other users."),
    ("HTTP Host Header Attacks", "host-header", 7, 1, 4.0, "Manipulating the Host header for cache poisoning, malicious password resets, and routing bugs."),
    ("HTTP Request Smuggling", "request-smuggling", 22, 3, 5.5, "One of the hardest and most valuable classes today; a parsing mismatch between proxy and server."),
    ("OAuth Authentication", "oauth", 6, 1, 4.0, "Common flaws in OAuth 2.0 implementations and account takeover."),
    ("JWT Attacks", "jwt", 8, 1, 5.0, "Algorithm manipulation, weak keys, and JSON Web Token signature bypasses."),
    ("Prototype Pollution", "prototype-pollution", 10, 2, 4.0, "Polluting JavaScript prototypes, both client-side and server-side (Node.js)."),
    ("Web LLM Attacks", "llm-attacks", 7, 1, 4.0, "An emerging class: prompt injection and vulnerabilities in LLM-based applications."),
]

for name, slug, labs, ndays, hpd, desc in swigger_topics:
    for i in range(ndays):
        part = f" — part {i+1} of {ndays}" if ndays > 1 else ""
        d(p5, f"{name}{part}",
          f"{desc} Today, solve roughly {round(labs/ndays)} labs from '{name}' on PortSwigger Academy on your own; if you're stuck after 30 minutes, only look at the hint, not the full solution. This is a real, long study session — not a quick drill, so budget the time. Write a short summary (what it was, how it was found, how it's fixed) in Obsidian for each vulnerability you solve.",
          [R(f"PortSwigger Academy — {name}", f"https://portswigger.net/web-security/{slug}"),
           R("PayloadsAllTheThings — ready-made payloads for this vulnerability class", "https://github.com/swisskyrepo/PayloadsAllTheThings")],
          hours=hpd, kind="practice")

d(p5, "Big review: rebuild every vulnerability on DVWA",
  "On your local DVWA, implement at least one example of every vulnerability class you've learned (SQLi, XSS, CSRF, IDOR, SSRF...) from scratch, without looking at notes.",
  [R("DVWA (free)", "https://github.com/digininja/DVWA")], hours=3, kind="review")
d(p5, "Big checkpoint: full Web Security Academy sweep",
  "Go back to PortSwigger Academy's 'All Topics' page and finish any lab still unsolved. Goal: your Academy progress bar should be above 80%.",
  [R("PortSwigger — All Topics", "https://portswigger.net/web-security/all-topics")], hours=3, kind="milestone")

# ===========================================================================
p6 = phase("p6", "Focused Practice: Voorivex & Hacker101 CTF", "Time to put the theory to the test with focused Persian-community content and a real CTF", "🕹️", "#0891b2")
d(p6, "Finish Yashar Shahinzadeh's free course",
  "Complete the 'Free Application Security from Scratch' course on Maktabkhooneh. Anything you've heard repeated but aren't sure about, look up again on PortSwigger.",
  [R("Yashar's free course on Maktabkhooneh", "https://maktabkhooneh.org/search/?q=%D8%A7%D9%85%D9%86%DB%8C%D8%AA+%D8%A7%D9%BE%D9%84%DB%8C%DA%A9%DB%8C%D8%B4%D9%86+%D8%A7%D8%B2+%D8%B5%D9%81%D8%B1")], hours=3, kind="learn")
d(p6, "Go through the Voorivex Team blog and socials",
  "Read every technical post on the Voorivex Team blog and follow Yashar Shahinzadeh on X for new writeups.",
  [R("Voorivex Team blog", "https://blog.voorivex.team/"), R("Yashar Shahinzadeh on X", "https://x.com/yshahinzadeh")], hours=2, kind="learn")
d(p6, "Note: Voorivex Academy courses are paid",
  "Voorivex Academy's official courses (e.g. OWASP ZeroX) are paid live classes, not free — no need to register or pay. Just glance at the course page to see their curriculum structure for inspiration, and spend your time on the same founders' genuinely free YouTube/blog content instead.",
  [R("Voorivex Academy course page (for reference only)", "https://voorivex.academy/"), R("Voorivex YouTube channel (fully free)", "https://www.youtube.com/@Voorivex")], hours=1, kind="learn")
d(p6, "Hacker101 CTF — sign up and first challenge",
  "Sign up for Hacker101 CTF and solve the first (usually easiest) challenge without outside help.",
  [R("Hacker101 CTF (free)", "https://ctf.hacker101.com/")], hours=3, kind="practice")
d(p6, "Hacker101 CTF — tier 2 challenges",
  "Move to the more complex Hacker101 CTF challenges. Document every challenge in detail in Obsidian, solved or not — this is direct practice for writing professional reports.",
  [R("Hacker101 CTF", "https://ctf.hacker101.com/")], hours=3, kind="practice")
d(p6, "Hacker101 CTF — advanced challenges",
  "Work on the hardest remaining challenges. If you're genuinely stuck after real effort, search for public Hacker101 write-ups — but only read them after trying yourself.",
  [R("Hacker101 — Resources section", "https://www.hacker101.com/resources")], hours=3, kind="practice")
d(p6, "Google XSS Game and Google Gruyere",
  "Solve Google's two free practice environments; XSS Game focuses specifically on XSS and Gruyere is a full vulnerable app with varied challenges.",
  [R("Google XSS Game (free)", "https://xss-game.appspot.com/"), R("Google Gruyere (free)", "https://google-gruyere.appspot.com/")], hours=3, kind="practice")
d(p6, "OverTheWire Natas — levels 0-7 (web-specific wargame)",
  "Unlike Bandit which is Linux-focused, Natas targets web vulnerabilities directly (View Source, PHP, cookies, headers). Solve levels 0-7 using your browser and View-Source.",
  [R("OverTheWire Natas (free)", "https://overthewire.org/wargames/natas/")], hours=3, kind="practice")
d(p6, "OverTheWire Natas — levels 8-15",
  "Solve the mid-tier Natas levels: PHP type-comparison bypasses, command injection, and simple logic bugs in PHP code.",
  [R("OverTheWire Natas (free)", "https://overthewire.org/wargames/natas/")], hours=3, kind="practice")
d(p6, "HackTheBox — free account and Starting Point Tier 0",
  "Create a free HackTheBox account (no VIP needed) and solve the Starting Point Tier 0 machines; each one ships with an official free step-by-step guide.",
  [R("Hack The Box — Starting Point (free)", "https://app.hackthebox.com/starting-point"), R("Starting Point intro guide", "https://help.hackthebox.com/en/articles/6007919-introduction-to-starting-point")], hours=3, kind="practice")
d(p6, "HackTheBox — Starting Point Tier 1",
  "Move to Tier 1 machines; slightly more complex than Tier 0, and they build your service-enumeration skills and ability to chain multiple vulnerabilities.",
  [R("Hack The Box — Starting Point (free)", "https://app.hackthebox.com/starting-point")], hours=3, kind="practice")
d(p6, "Bugcrowd University — videos and labs",
  "Watch any Bugcrowd University video modules you haven't seen yet, especially XSS, Access Control, and Burp Suite.",
  [R("Bugcrowd University (free)", "https://github.com/bugcrowd/bugcrowd_university")], hours=2, kind="learn")
d(p6, "Rana Khalil's YouTube — Web Security Academy series",
  "Watch Rana Khalil's free playlist solving each PortSwigger lab on video, for whichever labs you personally found hardest — a different way of thinking.",
  [R("Rana Khalil's YouTube channel", "https://www.youtube.com/@RanaKhalil101")], hours=2, kind="learn")
d(p6, "NahamSec's YouTube — Live Hacking videos",
  "Watch a few of NahamSec's free 'Live Hacking' videos to see the real thought process of a professional hunter working a real target.",
  [R("NahamSec's YouTube channel", "https://www.youtube.com/@NahamSec")], hours=2, kind="learn")
d(p6, "Phase wrap-up: a portfolio of what you've solved",
  "Compile every challenge/lab you've solved so far (Bandit, PortSwigger, Hacker101, DVWA, Natas, HackTheBox, Gruyere) into a 'Portfolio' page in Obsidian — the seed of your future resume.",
  [R("NahamSec's resource list (free, GitHub)", "https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters")], hours=2, kind="review")

# ===========================================================================
p7 = phase("p7", "Recon & Professional Hunting Methodology", "Before testing any vulnerability, map the full attack surface", "🔭", "#4d7c0f")
d(p7, "Jason Haddix — Bug Hunter's Methodology (full talk)",
  "Watch Jason Haddix's full 2-hour training with complete notes; one of the most respected free methodologies in bug bounty.",
  [R("The Bug Hunter's Methodology — full 2-hour talk (free)", "https://www.youtube.com/watch?v=uKWu6yhnhbQ")], hours=3, kind="learn")
d(p7, "Bug Hunter's Methodology v4 — Recon Edition",
  "Watch the recon-focused edition of this methodology and list every tool it introduces in Obsidian.",
  [R("Bug Hunter's Methodology v4.0 — Recon Edition (free)", "https://www.youtube.com/watch?v=p4JgIu1mceI")], hours=2, kind="learn")
d(p7, "Subdomain enumeration tools",
  "Install subfinder and amass and run them against a domain with a public bug bounty program (within program rules); compare their output.",
  [R("subfinder (free, ProjectDiscovery)", "https://github.com/projectdiscovery/subfinder"), R("OWASP Amass (free)", "https://github.com/owasp-amass/amass")], hours=3, kind="practice")
d(p7, "Probing live hosts: httpx",
  "Install httpx and pipe your subdomain list into it to see which hosts are alive, their status codes, and their tech stack.",
  [R("httpx (free, ProjectDiscovery)", "https://github.com/projectdiscovery/httpx")], hours=2, kind="practice")
d(p7, "Automated vulnerability scanning: nuclei",
  "Install nuclei, update its free community templates, and run it against authorized targets (within program scope); learn to spot false positives.",
  [R("nuclei (free, ProjectDiscovery)", "https://github.com/projectdiscovery/nuclei")], hours=3, kind="practice")
d(p7, "Content/path discovery: ffuf and wordlists",
  "Practice ffuf for directory/content discovery with SecLists wordlists; see the practical difference between parameter, path, and subdomain fuzzing.",
  [R("ffuf (free)", "https://github.com/ffuf/ffuf"), R("SecLists — ready-made wordlists (free)", "https://github.com/danielmiessler/SecLists")], hours=3, kind="practice")
d(p7, "Tomnomnom's tools and a combined recon pipeline",
  "Install tomnomnom's lightweight, powerful tools (waybackurls, gf, httprobe) and build a combined pipeline: subfinder | httpx | nuclei.",
  [R("tomnomnom's tools (free)", "https://github.com/tomnomnom"), R("waybackurls — URL discovery via web archive (free)", "https://github.com/tomnomnom/waybackurls")], hours=3, kind="practice")
d(p7, "Google Dorking and advanced OSINT",
  "Learn Google Dork techniques (site:, inurl:, filetype:) and OSINT for finding exposed sensitive files, admin panels, and forgotten subdomains.",
  [R("Google Hacking Database — GHDB (free)", "https://www.exploit-db.com/google-hacking-database")], hours=2, kind="practice")
d(p7, "Technology fingerprinting",
  "Practice Wappalyzer and whatweb for identifying a target's framework, CMS, and libraries — knowing the exact tech version is a direct path to known CVEs.",
  [R("Wappalyzer (free browser extension)", "https://www.wappalyzer.com/"), R("whatweb (free)", "https://github.com/urbanadventurer/WhatWeb")], hours=2, kind="practice")
d(p7, "Build your personal recon pipeline, final version",
  "Combine your Python tool from Phase 3 with your new tools (subfinder, httpx, nuclei) into a single Bash/Python script that runs your entire initial recon flow on one input domain.",
  [R("Reference automated recon pipeline (free, GitHub)", "https://github.com/six2dez/reconftw")], hours=3, kind="milestone")
d(p7, "Pick your first real bug bounty target",
  "Based on scope, competition level, and app type, choose a real bug bounty program (HackerOne/Bugcrowd) or VDP you'll focus on in the coming phases. Read its scope and rules of engagement in full.",
  [R("HackerOne — Program Directory", "https://hackerone.com/directory/programs"), R("Bugcrowd — Programs", "https://bugcrowd.com/programs")], hours=2, kind="review")
d(p7, "First full recon pass on a real target",
  "Run your recon pipeline against your chosen target (strictly within authorized scope). Categorize the results in Obsidian: subdomains, tech stack, API endpoints, and suspicious entry points.",
  [R("Recon checklist — Voorivex Bug Bounty Roadmap", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")], hours=3, kind="practice")

# ===========================================================================
p8 = phase("p8", "Mobile & Advanced API Security", "Many bug bounty programs today include mobile apps and APIs — less competition, often higher payouts", "📱", "#9333ea")
d(p8, "Intro to OWASP MASVS/MASTG",
  "Review the OWASP Mobile Application Security standard (MASVS) and its testing guide (MASTG) as your mobile security roadmap.",
  [R("OWASP MASTG (free)", "https://mas.owasp.org/MASTG/")], hours=2, kind="learn")
d(p8, "Set up an Android testing environment",
  "Install Android Studio and an AVD (Android emulator, free), learn ADB, and install a practice vulnerable app (AndroGoat) on the emulator.",
  [R("AndroGoat — free practice app (GitHub)", "https://github.com/satishpatnayak/AndroGoat"), R("Android Studio (free)", "https://developer.android.com/studio")], hours=3, kind="practice")
d(p8, "Intercepting mobile app traffic with Burp",
  "Set Burp Suite as the emulator's proxy, install the CA certificate, and intercept AndroGoat's traffic — the exact technique for testing any real mobile app.",
  [R("PortSwigger — configuring Burp for mobile", "https://portswigger.net/burp/documentation/desktop/mobile")], hours=3, kind="practice")
d(p8, "Decompiling and static analysis of an Android app",
  "Decompile an APK with jadx and look for hardcoded secrets (API keys, server addresses, passwords) in the code.",
  [R("jadx — free Android decompiler", "https://github.com/skylot/jadx")], hours=3, kind="practice")
d(p8, "Insecure data storage and SSL pinning bypass",
  "Check what data an app stores insecurely (SharedPreferences, local DB), and learn SSL pinning and free bypass techniques (Frida/Objection).",
  [R("OWASP MASTG — Testing Network Communication", "https://github.com/OWASP/mastg/blob/master/Document/0x05g-Testing-Network-Communication.md"), R("Objection (free)", "https://github.com/sensepost/objection")], hours=3, kind="practice")
d(p8, "OWASP API Security Top 10",
  "Read the 2023 OWASP API Security Top 10 in full — the dedicated roadmap for API vulnerabilities, extremely valuable in bug bounty today.",
  [R("OWASP API Security Project (free)", "https://owasp.org/www-project-api-security/")], hours=2, kind="learn")
d(p8, "BOLA/IDOR in APIs",
  "Practice Broken Object Level Authorization (BOLA) — the most common real-world API bug — with PortSwigger's practical labs.",
  [R("PortSwigger — API Testing Labs", "https://portswigger.net/web-security/api-testing")], hours=3, kind="practice")
d(p8, "Deep-dive GraphQL security",
  "Go deeper on introspection queries, batching attacks, and IDOR in GraphQL with PortSwigger's free labs.",
  [R("PortSwigger — GraphQL API vulnerabilities", "https://portswigger.net/web-security/graphql")], hours=3, kind="practice")
d(p8, "APIsec University — free API security courses",
  "Work through APIsec University's free courses, especially the introductory API Penetration Testing course.",
  [R("APIsec University (free, sign-up required)", "https://www.apisecuniversity.com/")], hours=2, kind="learn")
d(p8, "Phase capstone: full test of a free public API",
  "Using Postman or Burp, fully assess a public practice API (e.g. OWASP Juice Shop): enumerate every endpoint, break auth, and hunt for BOLA.",
  [R("OWASP Juice Shop — fully vulnerable practice app (free)", "https://owasp.org/www-project-juice-shop/")], hours=3, kind="milestone")

# ===========================================================================
p9 = phase("p9", "Real Hunting & Professional Reporting", "From here on you work real programs; report quality matters as much as the bug itself", "🏹", "#b45309")
d(p9, "Anatomy of a professional bug bounty report",
  "Learn the standard structure of a good report (Title, Summary, Steps to Reproduce, Impact, Remediation, PoC) from HackerOne's guide and build your own template in Obsidian.",
  [R("HackerOne — writing a quality report (free)", "https://docs.hackerone.com/en/articles/8475116-quality-reports"), R("Bugcrowd Vulnerability Rating Taxonomy", "https://bugcrowd.com/vulnerability-rating-taxonomy")], hours=2, kind="learn")
d(p9, "Deep-read 10 top disclosed reports",
  "Read 10 top-rated disclosed reports on HackerOne Hacktivity and analyze each: how was the bug found, why was impact high, how was the report written?",
  [R("HackerOne Hacktivity", "https://hackerone.com/hacktivity"), R("Awesome Bugbounty Writeups (free)", "https://github.com/devanshbatham/Awesome-Bugbounty-Writeups")], hours=2, kind="learn")
d(p9, "Hunt day 1: authentication and access control",
  "On your chosen target, focus fully on authentication, session management and IDOR. Log every suspicious path in Obsidian even if you're not sure it's a bug.",
  [R("Authentication testing checklist — PortSwigger", "https://portswigger.net/web-security/authentication")], hours=3, kind="practice")
d(p9, "Hunt day 2: input testing for XSS and injection",
  "Fuzz every input field, URL parameter, and controllable header of the target for XSS and injection types with Burp Intruder.",
  [R("PayloadsAllTheThings — XSS", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection")], hours=3, kind="practice")
d(p9, "Hunt day 3: business logic testing",
  "Test the target's multi-step flows (checkout, discounts, referrals, plan upgrades) for logic bugs — no scanner finds these, and they often pay well.",
  [R("PortSwigger — Business logic vulnerabilities", "https://portswigger.net/web-security/logic-flaws")], hours=3, kind="practice")
d(p9, "Hunt day 4: API and mobile-related endpoints",
  "If the target has a mobile app or public API, apply your Phase 8 skills to it; otherwise go deeper on the attack surface you mapped in Phase 7's recon.",
  [R("API testing checklist — PortSwigger", "https://portswigger.net/web-security/api-testing")], hours=3, kind="practice")
d(p9, "Write your first full report (even a low-severity VDP find)",
  "Report anything you've found so far — even a low-risk bug — using the professional format you built on day one of this phase. Add a clear PoC (screenshot or short screen recording).",
  [R("Free screen-recording tools — OBS Studio", "https://obsproject.com/")], hours=3, kind="milestone")
d(p9, "Learning from rejected reports (Duplicate/N-A)",
  "Read HackerOne's docs on common rejection reasons (Duplicate, Informative, Not Applicable, Out of Scope) so you approach triage with the right mindset and don't get discouraged.",
  [R("HackerOne — Report States", "https://docs.hackerone.com/en/articles/8475030-report-states")], hours=1, kind="learn")
d(p9, "Hunt day 5: focus on one specialized vulnerability class",
  "Pick one of the lower-competition classes you learned in Phase 5 (race conditions, SSRF, or request smuggling) and test the target specifically for it.",
  [R("PortSwigger — Race Conditions", "https://portswigger.net/web-security/race-conditions")], hours=3, kind="practice")
d(p9, "Expand your hunting scope: pick targets 2 and 3",
  "Choose two more bug bounty programs (ideally with a different tech stack than your first target) to increase your recon/testing speed and gain variety.",
  [R("HackerOne Directory", "https://hackerone.com/directory/programs")], hours=2, kind="practice")
d(p9, "Sustained hunting and building a daily habit",
  "Set a fixed daily or weekly time block for ongoing hunting. Log every finding (bug or not) in Obsidian tagged (Confirmed/Duplicate/Triaged/Rejected) to track your real progress.",
  [R("Example bug bounty tracker template", "https://www.notion.so/templates/bug-bounty-tracker")], hours=3, kind="practice")
d(p9, "Build a resume and public hunter profile",
  "Write a short security resume and make your GitHub profile (with the recon tools you built along the way) public — this portfolio directly affects future job opportunities.",
  [R("Resume inspiration — NahamSec Resources", "https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters")], hours=2, kind="review")

# ===========================================================================
p10 = phase("p10", "Advanced Topics & Continuous Growth", "The road doesn't 'end' here — this phase is your framework for lifelong learning", "♾️", "#1e293b")
d(p10, "HTTP/2 and HTTP/3 from a security angle",
  "Read James Kettle's research on the differences between HTTP/2 and HTTP/1.1 and their security implications, especially for request smuggling.",
  [R("James Kettle — HTTP/2: The Sequel is Always Worse (free, PortSwigger Research)", "https://portswigger.net/research/http2")], hours=3, kind="learn")
d(p10, "HTTP Desync Attacks and Web Cache Poisoning — the original research",
  "Read James Kettle's two foundational papers on request smuggling and cache poisoning — the industry's primary references in this area.",
  [R("HTTP Desync Attacks (free)", "https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn"), R("Practical Web Cache Poisoning (free)", "https://portswigger.net/research/practical-web-cache-poisoning")], hours=3, kind="learn")
d(p10, "Differential parsing: Orange Tsai's research",
  "Watch/read Orange Tsai's famous 'Breaking Parser Logic' talk and the Nginx off-by-slash example — a masterclass in creative bug-finding.",
  [R("Orange Tsai — Breaking Parser Logic slides (free, GitHub)", "https://github.com/orangetw/My-Presentation-Slides/blob/main/data/2018-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out.pdf"), R("Full DEF CON 26 talk video (free)", "https://www.youtube.com/watch?v=28xWcRegncw")], hours=2, kind="learn")
d(p10, "Reverse proxies and weird proxy behavior",
  "Review Aleksei Tiurin's 'weird_proxies' research on unexpected reverse-proxy behavior — inspiration for finding custom bugs in complex architectures.",
  [R("weird_proxies — GitHub (free)", "https://github.com/GrrrDog/weird_proxies")], hours=2, kind="learn")
d(p10, "OAuth 2.0 in depth",
  "Review deeper OAuth concepts (Authorization Code Flow, PKCE, state parameter) so you can spot more complex OAuth bugs too.",
  [R("OAuth 2.0 Simplified — free online guide", "https://www.oauth.com/")], hours=2, kind="learn")
d(p10, "Build your own vulnerable app with a framework",
  "Build a small app with Django or Laravel (both free) and deliberately plant a few vulnerabilities — building a bug yourself deepens your understanding of exploiting it.",
  [R("Django (free)", "https://www.djangoproject.com/"), R("Laravel (free)", "https://laravel.com/")], hours=3, kind="practice")
d(p10, "Web LLM Attacks — going deeper",
  "Revisit PortSwigger's Web LLM Attacks labs and follow new research on prompt injection — this field is evolving fast.",
  [R("PortSwigger — Web LLM Attacks", "https://portswigger.net/web-security/llm-attacks")], hours=2, kind="learn")
d(p10, "Enter a real CTF",
  "Sign up for a free, public CTF competition (via CTFtime) and spend at least a few hours working web challenges, solo or with a team.",
  [R("CTFtime — CTF competition calendar (free)", "https://ctftime.org/"), R("picoCTF — always-on free CTF", "https://picoctf.org/")], hours=4, kind="practice")
d(p10, "Follow daily web security news",
  "Build a daily news-source list (top researchers on X, free newsletters like tl;dr sec) and turn it into a 15-minute daily habit.",
  [R("tl;dr sec — free security newsletter", "https://tldrsec.com/"), R("PortSwigger Research Blog (free)", "https://portswigger.net/research")], hours=1, kind="learn")
d(p10, "Final review and update of your personal methodology",
  "Revisit and rewrite the Methodology document you started on day one in Obsidian. It should now be a fully personalized hunting methodology you follow on every engagement.",
  [R("Voorivex Bug Bounty Roadmap — for final inspiration", "https://blog.voorivex.team/bug-bounty-roadmap-from-scratch")], hours=2, kind="review")
d(p10, "Final wrap-up and your next 6 months",
  "Write a final document: what you learned, which vulnerability classes you're strongest in, and your plan for the next 6 months (specializing in one area, joining private programs, or an AppSec career path). This isn't the end — it's the starting point of your professional hunting career.",
  [R("NahamSec's full resource list to keep going", "https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters")], hours=2, kind="milestone")

# ===========================================================================
pAI = phase("pai", "AI in Bug Bounty", "AI is both a new attack surface you must understand, and a tool that will wreck your reputation if you misuse it", "🤖", "#f43f5e")
d(pAI, "The real state of AI in bug bounty today",
  "Start with facts, not hype: most professional hunters today use AI to speed up recon, code analysis, and report writing — but low-quality 'AI slop' reports have made programs like curl shut down their bug bounty entirely. Fully understand this tension before you use AI yourself.",
  [R("HackerOne — official blog on AI and Hai", "https://www.hackerone.com/blog"), R("Google Project Zero — a real vulnerability found by AI (Big Sleep)", "https://projectzero.google/2024/10/from-naptime-to-big-sleep.html")], hours=2, kind="learn")
d(pAI, "OWASP Top 10 for LLM Applications",
  "Read OWASP's official, free list of LLM application vulnerabilities (Prompt Injection, Insecure Output Handling, Training Data Poisoning, etc.) in full — the reference framework for this entire phase.",
  [R("OWASP Top 10 for LLM Applications (free, official)", "https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/")], hours=3, kind="learn")
d(pAI, "Hands-on prompt injection: the Gandalf game",
  "Solve Lakera's free, interactive Gandalf game from level zero to the final level (Gandalf the White). The best free way in the world to build a hands-on intuition for prompt injection, not just theory.",
  [R("Gandalf — free prompt injection game", "https://gandalf.lakera.ai/")], hours=3, kind="practice")
d(pAI, "Revisit PortSwigger Web LLM Attacks with an attacker mindset",
  "Return to the Web LLM Attacks labs you solved in the core vulnerabilities phase, but this time focus on indirect prompt injection (when the payload is injected from a third-party source like an email or web page) and chaining it with SSRF/exfiltration.",
  [R("PortSwigger — Web LLM attacks", "https://portswigger.net/web-security/llm-attacks"), R("Embrace The Red — independent prompt injection research (free)", "https://embracethered.com/blog/")], hours=4, kind="practice")
d(pAI, "Specialized free resource: Simon Willison's blog",
  "Simon Willison is one of the most respected independent voices in LLM security. Read his full free prompt-injection tag archive — he was the first to precisely formalize this attack class.",
  [R("Simon Willison — prompt injection archive (free)", "https://simonwillison.net/tags/prompt-injection/")], hours=3, kind="learn")
d(pAI, "MCP (Model Context Protocol) security — the 2026 emerging attack surface",
  "MCP is the standard protocol connecting tools to AI models and is fast becoming a serious attack surface (command injection, tool poisoning, over-permissioned access). Read the official security docs and understand why dozens of CVEs have hit MCP servers in the past few months.",
  [R("Model Context Protocol — official docs (free)", "https://modelcontextprotocol.io/"), R("OWASP GenAI Security Project (free)", "https://genai.owasp.org/")], hours=3, kind="learn")
d(pAI, "AI as a recon assistant: summarizing and prioritizing targets",
  "Feed the raw output of one of your earlier scans (subfinder/httpx/nuclei) to a language model (Claude or similar, free tier) and ask it to summarize, categorize, and risk-prioritize the output. This saves hours of manual log analysis — but always verify the model's output with your own eyes.",
  [R("Anthropic — official Claude docs (free to start)", "https://docs.claude.com/")], hours=3, kind="practice")
d(pAI, "AI as a code review assistant",
  "Review a small open-source project (or your own vulnerable app from Phase 10) with AI help, looking for unsafe patterns (SQL string concatenation, eval on user input, uncontrolled file paths); then re-check the findings with the free open-source tool Semgrep to see what the model got right or wrong.",
  [R("Semgrep — free open-source static analysis tool", "https://semgrep.dev/")], hours=3, kind="practice")
d(pAI, "Writing reports with AI — correctly, not as slop",
  "Learn to use AI to polish the writing, structure, and clarity of reports for bugs you found entirely by hand and manually verified — never to fabricate a finding. Read HackerOne's Good Faith AI Research rules in full to understand where the legal/ethical line is.",
  [R("HackerOne — Good Faith AI Research Safe Harbor", "https://www.hackerone.com/policies")], hours=2, kind="learn")
d(pAI, "Phase capstone: an AI helper script for your methodology",
  "Write a small Python script that takes the output of your Phase 7 recon.py, uses a free/cheap language model API to do a first-pass categorization, and saves a Markdown summary report. Add this tool to your personal GitHub repo.",
  [R("Anthropic API — docs (free to start, pay-as-you-go)", "https://docs.claude.com/en/api/overview")], hours=3, kind="milestone")

COMPACTION_TARGETS = {
    "p0": 5, "p1": 10, "p2": 10, "p3": 10, "p4": 8,
    "p5": None, "p6": 10, "p7": 9, "p8": 8, "p9": 9, "p10": 8, "pai": 11,
}

day_counter = 0
for p in phases:
    target = COMPACTION_TARGETS.get(p["id"])
    if target is not None:
        p["days"] = compact(p["days"], target)
    for day in p["days"]:
        day_counter += 1
        day["day"] = day_counter

out = {"generated_days": day_counter, "phases": phases}

os.makedirs("data", exist_ok=True)
with open("data/roadmap.en.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

total_hours = sum(day["hours"] for p in phases for day in p["days"])
print(f"OK: {len(phases)} phases, {day_counter} days, {round(total_hours)}h total written to data/roadmap.en.json")
for p in phases:
    print(f"  {p['id']:5s} {p['title']:50s} {len(p['days']):3d} days")
