# Insider Threat Detection (Typing-based)

A small research/demo project that uses typing biometrics and keystroke logging to detect anomalous or suspicious typing behavior. Includes a Streamlit dashboard for user/admin views, simple typing-pr...

## Table of contents

- [Features](#features)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [Setup & run](#setup--run)
- [Important notes & security](#important-notes--security)
- [Customization](#customization)
- [License](#license)

## Features

- Capture typing behavior and derive statistical typing profiles.
- Register users and verify typing sessions against stored profiles (anomaly detection).
- Keystroke logger that writes hold times and timestamps to `k.csv`.
- Streamlit dashboard with separate Admin and User views, and logging of typing-test results to a local SQLite DB.

## Repository structure

- `continuous_auth.py` — CLI script to collect typing samples and save a simple profile (hold/flight statistics).
- `typing_auth.py` — Registration and verification flow using more features (key latencies, error rate, simple IsolationForest anomaly detection). Can send alerts on anomalies.
- `keystroke_logger.py` — Low-level key capture that logs each key's hold time to `k.csv` next to the script. Stops on Esc.
- `dashboard.py` — Streamlit app (Admin/User) that stores users and typing test results in `users.db` and can send alerts for high/critical suspicion.
- `SETUP_NOTES.md` — Important repository-specific setup and notes (cleanup performed, file name fixes, OS/permission notes).
- `requirements.txt` — Python dependencies used by the project.

## Requirements

- Python 3.8+ recommended
- See `requirements.txt` for libraries; install with:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Common dependencies include: streamlit, pynput, numpy, scikit-learn, plotly, pandas, requests, bcrypt, pillow

## Setup & run

1. Create and activate a virtual environment and install requirements (see above).
2. Read `SETUP_NOTES.md` — it contains important fixes and platform-specific guidance (macOS input monitoring, Linux permissions, and other notes).
3. Register a user profile (example):

```bash
python continuous_auth.py
# or for the menu-driven flow
python typing_auth.py
```

4. Collect raw keystroke logs (locally, with keyboard attached):

```bash
python keystroke_logger.py
# Logs to k.csv next to the script; press ESC to stop.
```

5. Run the Streamlit dashboard (opens on localhost:8501):

```bash
streamlit run dashboard.py
```

User workflow: Sign up or register a username, go to User Dashboard → Start Test → type and Submit. Admins can view `Admin Dashboard` to see recent typing test results.

## Results
Register
<img width="1805" height="912" alt="image" src="https://github.com/user-attachments/assets/38f3f213-afd6-4599-b189-1d2ca03f9e75" />
Verify
<img width="1666" height="952" alt="image" src="https://github.com/user-attachments/assets/4e0ee8fe-648c-4d5f-ab46-b39d138d2ac5" />
Dashboard
<img width="1887" height="806" alt="image" src="https://github.com/user-attachments/assets/0b910728-ef4a-4fcd-9647-13e2294e4da9" />
<img width="1892" height="956" alt="image" src="https://github.com/user-attachments/assets/e3402223-8711-4aed-8e10-847302f7133b" />

## Important notes & security

- This project uses `pynput` to capture keyboard events. Run these scripts only on machines you own and understand: keystroke capture is sensitive and can be misused.
- On macOS you must grant "Input Monitoring" / Accessibility permission to the terminal or IDE used to run the scripts.
- On some Linux distributions capturing global input requires root privileges.
- The code contains a hardcoded webhook URL used to send alert POSTs from `typing_auth.py` and `dashboard.py`. Replace the webhook URL in the scripts if you want to use your own.
- `dashboard.py` stores users and typing logs in `users.db` (SQLite) in the working directory. Treat this as sensitive data.
- The project is a demo/proof-of-concept and not intended for production use. Do not deploy key-logging code on production systems.

## Customization

- To change the webhook URL, update it near the top of `typing_auth.py` and `dashboard.py`.
- To change the sample text or number of samples, edit `SAMPLE_TEXTS`, `VERIFICATION_TEXT`, and `NUM_SAMPLES` in `typing_auth.py` (or SAMPLE_TEXT in `continuous_auth.py`).
- The anomaly decision threshold is defined by `ANOMALY_THRESHOLD` in `typing_auth.py`.

## Troubleshooting

- If the Streamlit dashboard shows no user data, register a `user` account and complete at least one typing test from the User Dashboard.
- If `pynput` captures nothing on macOS, check system privacy settings (Input Monitoring / Accessibility) and restart the terminal/IDE after granting permissions.
- If file names contain spaces or parentheses (older copies of the repo), see `SETUP_NOTES.md` — this repo has been cleaned up and filenames fixed.

## License

This project is provided as-is for research/demo purposes. No license file is included; if you want a permissive license added (MIT/Apache2), open an issue or submit a PR.


---

If you'd like, I can also:
- add a CONTRIBUTING.md or LICENSE file,
- parameterize any webhook URL into an environment variable,
- or split the dashboard DB initialization into a separate setup script.
