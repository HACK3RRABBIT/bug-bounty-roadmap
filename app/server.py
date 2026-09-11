#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bug Bounty Roadmap — functional local prototype
Flask + SQLite: registration, login, roles (user/admin), per-user progress &
time tracking, an admin panel (post updates, toggle maintenance mode, manage
users), a notification system, and a custom 404 page.

Run:
    cd app && ../app/.venv/bin/python server.py
Serves on http://0.0.0.0:9876/

SECURITY NOTE: this is a learning-focused local prototype, not a hardened
production deployment. It binds to 0.0.0.0 so other devices on your LAN can
reach it — do not expose this port to the public internet as-is.
"""
import json
import os
import secrets
import sqlite3
import functools
from datetime import datetime, date, UTC

from flask import (
    Flask, g, request, session, redirect, url_for, render_template,
    flash, abort, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(REPO_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "bugbounty.db")

app = Flask(__name__)
app.secret_key = os.environ.get("BBR_SECRET_KEY") or secrets.token_hex(32)

# ---------------------------------------------------------------------------
# Content: reuse the exact same JSON the public static site uses — single
# source of truth, so the app never drifts out of sync with the roadmap.
# ---------------------------------------------------------------------------
def load_json(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)

ROADMAP = {"fa": load_json("roadmap.json"), "en": load_json("roadmap.en.json")}
CHANGELOG = load_json("changelog.json")

def phase_by_id(lang, pid):
    return next((p for p in ROADMAP[lang]["phases"] if p["id"] == pid), None)

def day_by_id(lang, day_id):
    for p in ROADMAP[lang]["phases"]:
        for d in p["days"]:
            if d["day"] == day_id:
                return d, p
    return None, None

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    last_seen_update INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    day_id INTEGER NOT NULL,
    lang TEXT NOT NULL DEFAULT 'fa',
    done_at TEXT NOT NULL,
    PRIMARY KEY (user_id, day_id)
);
CREATE TABLE IF NOT EXISTS timelog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    day_id INTEGER NOT NULL,
    the_date TEXT NOT NULL,
    minutes INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

def init_db():
    first_time = not os.path.exists(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    if first_time:
        db.execute("INSERT INTO settings(key, value) VALUES ('maintenance', '0')")
        now = datetime.now(UTC).isoformat()
        for item in CHANGELOG[::-1]:  # oldest first so ids grow chronologically-ish
            db.execute(
                "INSERT INTO updates(title, body, created_at) VALUES (?, ?, ?)",
                (item.get("title_en", item.get("title_fa", "")),
                 item.get("body_en", item.get("body_fa", "")), now),
            )
        db.commit()
    db.close()

def get_setting(key, default=None):
    row = get_db().execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default

def set_setting(key, value):
    db = get_db()
    db.execute("INSERT INTO settings(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
    db.commit()

# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def current_user():
    uid = session.get("uid")
    if not uid:
        return None
    return get_db().execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped(*a, **kw):
        if not current_user():
            flash("Please log in first.", "error")
            return redirect(url_for("login", next=request.path))
        return view(*a, **kw)
    return wrapped

def admin_required(view):
    @functools.wraps(view)
    def wrapped(*a, **kw):
        u = current_user()
        if not u or u["role"] != "admin":
            abort(403)
        return view(*a, **kw)
    return wrapped

@app.context_processor
def inject_globals():
    lang = session.get("lang", "fa")
    return dict(
        cur_user=current_user(),
        lang=lang,
        dir="rtl" if lang == "fa" else "ltr",
        maintenance_on=get_setting("maintenance", "0") == "1",
    )

@app.before_request
def maintenance_gate():
    if request.path.startswith("/static"):
        return
    if get_setting("maintenance", "0") == "1":
        u = current_user()
        allowed = request.path in ("/login", "/logout") or request.path.startswith("/admin")
        if not (u and u["role"] == "admin") and not allowed:
            return render_template("maintenance.html"), 503

# ---------------------------------------------------------------------------
# Routes: auth
# ---------------------------------------------------------------------------
@app.route("/set-lang/<lang>")
def set_lang(lang):
    if lang in ("fa", "en"):
        session["lang"] = lang
    return redirect(request.referrer or url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        error = None
        if not username or len(username) < 3:
            error = "Username must be at least 3 characters."
        elif not email or "@" not in email:
            error = "Enter a valid email."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        if not error:
            db = get_db()
            exists = db.execute("SELECT 1 FROM users WHERE username=? OR email=?", (username, email)).fetchone()
            if exists:
                error = "That username or email is already registered."
        if error:
            flash(error, "error")
            return render_template("register.html")
        db = get_db()
        is_first = db.execute("SELECT COUNT(*) c FROM users").fetchone()["c"] == 0
        role = "admin" if is_first else "user"
        db.execute(
            "INSERT INTO users(username, email, password_hash, role, created_at) VALUES (?,?,?,?,?)",
            (username, email, generate_password_hash(password), role, datetime.now(UTC).isoformat()),
        )
        db.commit()
        uid = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()["id"]
        session["uid"] = uid
        flash("Welcome! Your account was created." + (" You're the first user, so you're an admin." if is_first else ""), "ok")
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("index"))
    if request.method == "POST":
        identifier = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        row = db.execute("SELECT * FROM users WHERE username=? OR email=?", (identifier, identifier.lower())).fetchone()
        if row and check_password_hash(row["password_hash"], password):
            session["uid"] = row["id"]
            flash(f"Welcome back, {row['username']}.", "ok")
            nxt = request.args.get("next") or url_for("index")
            return redirect(nxt)
        flash("Wrong username/email or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("uid", None)
    flash("Logged out.", "ok")
    return redirect(url_for("index"))

# ---------------------------------------------------------------------------
# Routes: main app
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    lang = session.get("lang", "fa")
    u = current_user()
    done_ids = set()
    total_minutes = 0
    if u:
        rows = get_db().execute("SELECT day_id FROM progress WHERE user_id=?", (u["id"],)).fetchall()
        done_ids = {r["day_id"] for r in rows}
        tot = get_db().execute("SELECT COALESCE(SUM(minutes),0) s FROM timelog WHERE user_id=?", (u["id"],)).fetchone()
        total_minutes = tot["s"]
    phases = ROADMAP[lang]["phases"]
    total_days = ROADMAP[lang]["generated_days"]
    for p in phases:
        p_done = sum(1 for d in p["days"] if d["day"] in done_ids)
        p["_done"] = p_done
        p["_pct"] = round(p_done / len(p["days"]) * 100) if p["days"] else 0
    overall_pct = round(len(done_ids) / total_days * 100) if total_days else 0
    return render_template(
        "index.html", phases=phases, total_days=total_days,
        done_count=len(done_ids), overall_pct=overall_pct,
        total_hours_logged=round(total_minutes / 60, 1),
    )

@app.route("/phase/<pid>")
def phase_page(pid):
    lang = session.get("lang", "fa")
    p = phase_by_id(lang, pid)
    if not p:
        abort(404)
    u = current_user()
    done_ids, day_minutes = set(), {}
    if u:
        rows = get_db().execute("SELECT day_id FROM progress WHERE user_id=?", (u["id"],)).fetchall()
        done_ids = {r["day_id"] for r in rows}
        rows = get_db().execute(
            "SELECT day_id, COALESCE(SUM(minutes),0) m FROM timelog WHERE user_id=? GROUP BY day_id", (u["id"],)
        ).fetchall()
        day_minutes = {r["day_id"]: r["m"] for r in rows}
    return render_template("phase.html", phase=p, done_ids=done_ids, day_minutes=day_minutes)

@app.route("/toggle/<int:day_id>", methods=["POST"])
@login_required
def toggle_day(day_id):
    u = current_user()
    db = get_db()
    exists = db.execute("SELECT 1 FROM progress WHERE user_id=? AND day_id=?", (u["id"], day_id)).fetchone()
    lang = session.get("lang", "fa")
    if exists:
        db.execute("DELETE FROM progress WHERE user_id=? AND day_id=?", (u["id"], day_id))
    else:
        db.execute(
            "INSERT INTO progress(user_id, day_id, lang, done_at) VALUES (?,?,?,?)",
            (u["id"], day_id, lang, datetime.now(UTC).isoformat()),
        )
        # auto-log estimated hours the first time this day is completed
        already_logged = db.execute("SELECT 1 FROM timelog WHERE user_id=? AND day_id=?", (u["id"], day_id)).fetchone()
        if not already_logged:
            day, _ = day_by_id(lang, day_id)
            if day:
                db.execute(
                    "INSERT INTO timelog(user_id, day_id, the_date, minutes) VALUES (?,?,?,?)",
                    (u["id"], day_id, date.today().isoformat(), round(day["hours"] * 60)),
                )
    db.commit()
    return redirect(request.referrer or url_for("index"))

@app.route("/log-time/<int:day_id>", methods=["POST"])
@login_required
def log_time(day_id):
    try:
        minutes = int(request.form.get("minutes", 0))
    except ValueError:
        minutes = 0
    if minutes > 0:
        u = current_user()
        get_db().execute(
            "INSERT INTO timelog(user_id, day_id, the_date, minutes) VALUES (?,?,?,?)",
            (u["id"], day_id, date.today().isoformat(), minutes),
        )
        get_db().commit()
        flash(f"Logged {minutes} minutes.", "ok")
    return redirect(request.referrer or url_for("index"))

@app.route("/activity")
@login_required
def activity():
    u = current_user()
    rows = get_db().execute(
        "SELECT the_date, SUM(minutes) m FROM timelog WHERE user_id=? GROUP BY the_date", (u["id"],)
    ).fetchall()
    by_date = {r["the_date"]: r["m"] for r in rows}

    weeks = 20
    n_cells = weeks * 7
    today = date.today()
    start = date.fromordinal(today.toordinal() - n_cells + 1)
    cells = []
    active_days, total_minutes = 0, 0
    d = start
    for _ in range(n_cells):
        key = d.isoformat()
        mins = by_date.get(key, 0)
        level = 0
        if mins > 0: level = 1
        if mins >= 30: level = 2
        if mins >= 90: level = 3
        if mins >= 180: level = 4
        if mins > 0:
            active_days += 1
            total_minutes += mins
        cells.append({"date": key, "level": level, "hours": round(mins / 60, 1), "future": d > today})
        d = date.fromordinal(d.toordinal() + 1)

    recent = get_db().execute(
        "SELECT t.day_id, t.the_date, t.minutes FROM timelog t WHERE t.user_id=? ORDER BY t.id DESC LIMIT 15",
        (u["id"],),
    ).fetchall()
    lang = session.get("lang", "fa")
    recent_named = []
    for r in recent:
        day, phase = day_by_id(lang, r["day_id"])
        recent_named.append({"date": r["the_date"], "minutes": r["minutes"],
                              "title": day["title"] if day else f"Day {r['day_id']}",
                              "phase": phase["title"] if phase else ""})

    return render_template("activity.html", cells=cells, active_days=active_days,
                            total_hours=round(total_minutes / 60, 1), weeks=weeks, recent=recent_named)

# ---------------------------------------------------------------------------
# Routes: notifications
# ---------------------------------------------------------------------------
@app.route("/api/notifications")
def api_notifications():
    u = current_user()
    updates = get_db().execute("SELECT * FROM updates ORDER BY id DESC LIMIT 20").fetchall()
    last_seen = u["last_seen_update"] if u else 0
    unread = sum(1 for x in updates if x["id"] > last_seen)
    return jsonify(unread=unread, items=[dict(x) for x in updates])

@app.route("/notifications/seen", methods=["POST"])
@login_required
def notifications_seen():
    u = current_user()
    latest = get_db().execute("SELECT COALESCE(MAX(id),0) m FROM updates").fetchone()["m"]
    get_db().execute("UPDATE users SET last_seen_update=? WHERE id=?", (latest, u["id"]))
    get_db().commit()
    return jsonify(ok=True)

# ---------------------------------------------------------------------------
# Routes: admin
# ---------------------------------------------------------------------------
@app.route("/admin")
@admin_required
def admin_home():
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY id").fetchall()
    updates = db.execute("SELECT * FROM updates ORDER BY id DESC").fetchall()
    stats = {
        "users": len(users),
        "completions": db.execute("SELECT COUNT(*) c FROM progress").fetchone()["c"],
        "minutes_logged": db.execute("SELECT COALESCE(SUM(minutes),0) s FROM timelog").fetchone()["s"],
    }
    return render_template("admin.html", users=users, updates=updates, stats=stats)

@app.route("/admin/toggle-maintenance", methods=["POST"])
@admin_required
def admin_toggle_maintenance():
    cur = get_setting("maintenance", "0")
    set_setting("maintenance", "0" if cur == "1" else "1")
    flash("Maintenance mode " + ("disabled." if cur == "1" else "enabled."), "ok")
    return redirect(url_for("admin_home"))

@app.route("/admin/post-update", methods=["POST"])
@admin_required
def admin_post_update():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    if title and body:
        get_db().execute(
            "INSERT INTO updates(title, body, created_at) VALUES (?,?,?)",
            (title, body, datetime.now(UTC).isoformat()),
        )
        get_db().commit()
        flash("Update posted — all users will see it in their notification bell.", "ok")
    return redirect(url_for("admin_home"))

@app.route("/admin/set-role/<int:user_id>/<role>", methods=["POST"])
@admin_required
def admin_set_role(user_id, role):
    if role not in ("user", "admin"):
        abort(400)
    get_db().execute("UPDATE users SET role=? WHERE id=?", (role, user_id))
    get_db().commit()
    flash("Role updated.", "ok")
    return redirect(url_for("admin_home"))

# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

if __name__ == "__main__":
    init_db()
    print("Bug Bounty Roadmap app starting on http://0.0.0.0:9876")
    print("First account you register becomes admin automatically.")
    app.run(host="0.0.0.0", port=9876, debug=False)
