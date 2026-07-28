# Setup notes (read this first)

The original GitHub repo had files with spaces/parentheses in the names
(`continuous_auth (5).py`, `typing_auth (2).py`, `keystroke_logger (2).py`),
which is what was causing the "no proper folder" problem — command lines and
imports choke on those characters. This folder is the same code, just cleaned up:

- `continuous_auth (5).py`  → `continuous_auth.py`
- `typing_auth (2).py`      → `typing_auth.py`
- `keystroke_logger (2).py` → `keystroke_logger.py`
- `dashboard.py`            → unchanged
- Added `requirements.txt` (this wasn't in the repo, but the README referenced it)
- Fixed `keystroke_logger.py`: it had a hardcoded Windows path
  (`C:\Users\User\Downloads\k.csv`). It now writes `k.csv` next to the script,
  on any OS.

## How to run

1. Open a terminal in this folder.
2. (Recommended) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run whichever piece you need:
   ```bash
   python continuous_auth.py     # register a user's typing profile
   python typing_auth.py         # register/verify typing (menu-driven)
   python keystroke_logger.py    # log keystrokes to k.csv, ESC to stop
   streamlit run dashboard.py    # launch the web dashboard at localhost:8501
   ```

## Things to know before running

- `keystroke_logger.py` and the typing-capture parts of `continuous_auth.py` /
  `typing_auth.py` use `pynput`, which hooks your real keyboard. This only
  works when run **on your own machine with a keyboard/display** — it will
  not work in a headless server, a Docker container without a display, or an
  online notebook.
- On macOS you'll need to grant your terminal/IDE "Input Monitoring" /
  Accessibility permission the first time, or `pynput` will silently capture
  nothing.
- On Linux, keystroke capture may need to run as root/sudo depending on your
  distro's input permissions.
- `dashboard.py` (Streamlit) does **not** need keyboard permissions — that one
  should just work with `streamlit run dashboard.py`.
- `typing_auth.py` sends alerts to a Zapier webhook URL that's hardcoded in
  the script. If that webhook isn't yours/active, verification will still
  work locally, it just won't successfully notify anywhere — you can ignore
  that or swap in your own webhook URL.

## Dashboard changes (real data instead of fake demo data)

The original `dashboard.py` had two issues that made the Admin Dashboard
disconnected from reality:

1. The "Suspicious Activities Detected" table was 100% hardcoded
   (`user1`–`user4` with fixed made-up scores) — it never looked at who you'd
   actually registered.
2. The User Dashboard's WPM calculation measured elapsed time as roughly
   zero (it set `start_time = time.time()` and immediately used it), so the
   typing speed numbers were meaningless.

Fixed by:
- Adding a `typing_logs` table to `users.db` that stores each completed
  typing test (username, WPM, suspicion level, timestamp).
- User Dashboard now has a **Start Test** button (records the real start
  time) and a **Submit** button (computes real elapsed time), then saves the
  result to `typing_logs`.
- Admin Dashboard now queries the `users` table for real accounts with role
  `user`, and joins in each one's most recent `typing_logs` entry. If a user
  hasn't taken a test yet, they show up with "No data yet" instead of being
  silently omitted or replaced with fake data.

To see it work: sign up 1-2 accounts with role `user`, log in as each,
go to User Dashboard → Start Test → type something → Submit. Then log in as
an `admin` account and check Admin Dashboard — you should see your real
usernames and real scores.

## Zapier email alerts on the dashboard

`typing_auth.py` already sent a Zapier webhook alert on anomaly detection,
but `dashboard.py`'s User Dashboard test didn't — so completing a test there
never notified anyone. Added the same webhook call to `dashboard.py`: when a
user's typing test comes back **High** or **Critical**, it POSTs
`{"user_id": ..., "reason": ...}` to the same Zapier webhook URL used in
`typing_auth.py`, which is what you had wired to send an email before.

If you want to point it at a different Zap/webhook, just change
`ZAPIER_WEBHOOK_URL` near the top of `dashboard.py` (and in `typing_auth.py`
if you want both in sync).

Note: I did **not** include an Elasticsearch/MySQL logging variant that was
mixed into the file you shared — it referenced a `cursor`/`db` connection
that doesn't exist anywhere in this project and would crash on import. If
you actually want threats logged to Elasticsearch or MySQL in addition to
SQLite, let me know and I'll wire that up properly rather than drop in
broken code.
