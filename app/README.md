# Bug Bounty Roadmap — functional local app

A working local prototype of the roadmap as a real multi-user web app: registration,
login, roles (`user` / `admin`), per-user progress + time tracking, a notification
system, an admin panel, and maintenance-mode/404 handling. It reads the exact same
`data/roadmap.json` / `data/roadmap.en.json` / `data/changelog.json` the public static
site uses, so content never drifts between the two.

## Run it

```bash
cd app
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python server.py
```

Open **http://localhost:9876/** (or `http://<your-LAN-IP>:9876/` from another device on
your network — it binds `0.0.0.0`).

The **first account you register automatically becomes admin**. From `/admin` an admin
can: toggle maintenance mode (shows `maintenance.html` to everyone else), post a new
update (shows up as a notification-bell badge for every user), and promote/demote users.

## Features

- Registration/login with hashed passwords (`werkzeug.security`), session-based auth
- Roles: `user`, `admin` — admin-only routes return a proper `403` page
- Every phase opens as its own page (`/phase/<id>`) — not a JS tab, a real URL
- Per-user progress (checkbox) and a manual "log study time" tool per day
- A GitHub-style activity heatmap at `/activity`, computed server-side from real logs
- Notification bell reading admin-posted updates, with per-user "seen" tracking
- Custom `404` and `maintenance` pages
- FA/EN language toggle (session-based), same hacker-styled dark theme as the public site
- SQLite storage (`app/bugbounty.db`, gitignored — created on first run)

## Security notes (read before exposing this beyond your own machine)

This is a **learning-focused local prototype**, not a hardened production deployment:

- No rate limiting on login/register (add one — e.g. `flask-limiter` — before any
  public exposure).
- No CSRF tokens on forms (add `flask-wtf` for that in a real deployment).
- `app.secret_key` is randomly generated per process by default; set `BBR_SECRET_KEY`
  in the environment if you want sessions to survive a restart.
- Runs with `debug=False` already — never flip that on where anyone else can reach it.
- Binding `0.0.0.0:9876` makes it reachable from your local network, not the public
  internet, unless you've explicitly forwarded the port — don't do that without adding
  the hardening above first.

## Reset the database

```bash
rm app/bugbounty.db   # wipes all users/progress; a fresh one is created on next run
```
