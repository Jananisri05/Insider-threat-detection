# Insider Threat Detection System

A comprehensive Python-based security system for detecting and mitigating insider threats using behavioral analysis, continuous authentication, keystroke dynamics, and an interactive monitoring dashboard.

## 🎯 Overview

The Insider Threat Detection System is a sophisticated security solution that monitors user behavior patterns to identify potentially malicious activities in real-time. It combines multiple authentication mechanisms including:

- **Keystroke Dynamics Analysis** - Analyzes typing patterns and rhythms unique to each user
- **Continuous Authentication** - Monitors user behavior continuously throughout sessions
- **Typing Pattern Recognition** - Detects anomalies in typing speed, hold times, and flight times
- **Interactive Dashboard** - Real-time visualization and threat assessment interface
- **Anomaly Detection** - Uses Machine Learning (Isolation Forest) to identify suspicious behavior

## ✨ Key Features

- 🔐 **User Registration & Verification** - Secure enrollment using typing biometrics
- 📊 **Real-time Anomaly Detection** - Identifies deviations from baseline typing behavior
- 📈 **Interactive Dashboard** - Streamlit-based UI with admin and user interfaces
- 🔔 **Threat Alerting** - Zapier webhook integration for instant threat notifications
- 💾 **Keystroke Logging** - Detailed keystroke data collection and analysis
- 🎯 **Machine Learning** - Isolation Forest algorithm for anomaly scoring
- 👥 **Multi-user Support** - Manage multiple user profiles and baselines
- 🛡️ **Security First** - Password hashing with bcrypt, secure database storage

## 📋 Project Structure

```
Insider-threat-detection/
├── continuous_auth (5).py          # Continuous authentication and typing profile registration
├── typing_auth (2).py              # Typing behavior verification and anomaly detection
├── keystroke_logger (2).py         # Real-time keystroke logging and timing analysis
├── dashboard.py                    # Streamlit interactive dashboard
├── typing_profiles/                # User typing profile storage
├── users.db                        # SQLite user credentials database
└── README.md                       # Documentation
```

## 🔧 Components

### 1. **continuous_auth (5).py** - Typing Profile Registration

**Purpose:** Captures and stores baseline typing patterns for new users

**Features:**
- Registers users by collecting typing samples
- Calculates mean and standard deviation of hold times (key press duration)
- Calculates mean and standard deviation of flight times (time between keys)
- Stores profiles in CSV format for comparison

**Key Functions:**
```python
register_user(username)           # Registers new user with 2 typing samples
calculate_typing_profile()        # Extracts timing metrics from key events
```

**Usage:**
```bash
python "continuous_auth (5).py"
# Prompts for username and collects 2 typing samples
```

### 2. **typing_auth (2).py** - Verification & Anomaly Detection

**Purpose:** Verifies users by comparing current typing with stored profiles

**Features:**
- Compares real-time typing against stored baseline
- Uses Isolation Forest ML algorithm for anomaly detection
- Calculates comprehensive typing metrics:
  - Key latency (time between consecutive key presses)
  - Hold times (duration each key is pressed)
  - Flight times (time between key releases and next presses)
  - Typing speed (words per minute)
  - Error rate (backspace usage)
  - Special key usage (Shift, Ctrl, Alt combinations)
- Sends alerts via Zapier webhook when anomalies detected

**Key Functions:**
```python
register_user(username)           # Register with multiple sample texts
verify_user(username)             # Verify typing against stored profile
calculate_typing_profile(events)  # Extract 7 typing metrics
log_threat(user_id, reason)      # Send alerts via webhook
```

**Anomaly Detection Logic:**
- Uses StandardScaler for feature normalization
- Trains Isolation Forest on baseline profile
- Compares current session against baseline
- Flags if anomaly_score < -0.2

**Usage:**
```bash
python "typing_auth (2).py"
# Menu: 1=Register, 2=Verify
# Registers with 2 texts or verifies typing pattern
```

### 3. **keystroke_logger (2).py** - Real-time Keystroke Capture

**Purpose:** Logs all keystroke events with precise timing data

**Features:**
- Real-time monitoring of key presses and releases
- Captures hold time for each individual key
- Records timestamps in both human-readable and epoch formats
- Exports to CSV for analysis
- Supports special keys (Escape, Space, Ctrl, etc.)

**Data Logged:**
```
key_str         → The key pressed (e.g., 'a', 'Key.space')
human_time      → Formatted timestamp (YYYY-MM-DD HH:MM:SS)
epoch_time      → Unix timestamp with microseconds
hold_seconds    → Duration key was held down
```

**CSV Output Format:**
```
key_str,human_time,epoch_time,hold_seconds
a,2025-10-15 14:32:10,1755341530.123456,0.052341
```

**Usage:**
```bash
python "keystroke_logger (2).py"
# Starts logging to: C:\Users\User\Downloads\k.csv
# Press ESC to stop
```

### 4. **dashboard.py** - Interactive Monitoring Dashboard

**Purpose:** Provides real-time visualization and threat management interface

**Technology:** Streamlit with Plotly visualizations

**Features:**

#### Authentication
- User registration with role-based access (admin/user)
- Password hashing with bcrypt
- Session management

#### Admin Dashboard
- Displays suspicious activities table
- Real-time user risk scores
- Bar chart visualization of typing speed vs suspicion level
- Color-coded threat levels:
  - 🟢 Low: Green (#2ECC71)
  - 🟡 Moderate: Yellow (#F1C40F)
  - 🟠 High: Orange (#E67E22)
  - 🔴 Critical: Red (#E74C3C)

#### User Dashboard
- Text input area for typing analysis
- Real-time typing speed calculation (WPM)
- Suspicion level assessment based on typing speed
- Meme generation based on typing speed (gamification)

#### Settings Page
- Password change functionality
- User profile management

**Design:** Cyberpunk theme with:
- Dark background (#0d0d0d)
- Cyan accents (#00FFFF)
- Monospace fonts (Courier New)
- High contrast for visibility

## 🚀 Installation & Setup

### Prerequisites
```
Python 3.7+
Windows/Linux/Mac
Admin/elevated privileges (for keystroke logging)
```

### Step 1: Clone Repository
```bash
git clone https://github.com/Jananisri05/Insider-threat-detection.git
cd Insider-threat-detection
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
```
pynput              # Keyboard monitoring
numpy              # Numerical computations
scikit-learn       # Machine learning (Isolation Forest)
streamlit          # Dashboard UI
plotly             # Interactive visualizations
pandas             # Data manipulation
pillow             # Image handling
bcrypt             # Password hashing
requests           # HTTP requests for webhooks
```

### Step 3: Configure Settings

Edit the scripts to customize:
- `DATA_DIR`: Where typing profiles are stored
- `SAMPLE_TEXT`: Text users type during registration
- `ZAPIER_WEBHOOK_URL`: Endpoint for threat alerts
- `log_file`: Keystroke log location
- `ANOMALY_THRESHOLD`: Sensitivity for anomaly detection

### Step 4: Run Components

**Register a new user:**
```bash
python "continuous_auth (5).py"
# Enter username → Type sample text twice
```

**Verify user typing:**
```bash
python "typing_auth (2).py"
# Choose: 1=Register, 2=Verify → Follow prompts
```

**Start keystroke logging:**
```bash
python "keystroke_logger (2).py"
# Starts logging immediately, press ESC to stop
```

**Launch dashboard:**
```bash
streamlit run dashboard.py
# Opens at http://localhost:8501
```

## 📊 Data Files

### Typing Profiles (CSV)
```
typing_profiles/
├── user1.csv
├── user2.csv
└── user3.csv
```

**Profile format:**
```csv
metric,value
mean_hold_time,0.0523
std_hold_time,0.0124
mean_flight_time,0.0891
std_flight_time,0.0342
mean_key_latency,0.1234
...
```

### User Database (SQLite)
```
users.db
├── users table
   ├── id (INTEGER PRIMARY KEY)
   ├── username (TEXT UNIQUE)
   ├── password (TEXT, bcrypt hashed)
   └── role (TEXT: 'admin' or 'user')
```

### Keystroke Logs (CSV)
```
keystroke_logs/
└── k.csv
```

**Keystroke format:**
```csv
key_str,human_time,epoch_time,hold_seconds
a,2025-10-15 14:32:10,1755341530.123456,0.052341
b,2025-10-15 14:32:10,1755341530.175797,0.061234
...
```

## 🔐 Security Considerations

### ⚠️ Important Notes
1. **Requires Elevated Privileges** - Keystroke logging needs admin/root rights
2. **Privacy Compliance** - Ensure compliance with local data protection laws
3. **User Consent** - Get explicit consent before monitoring
4. **Data Protection** - Keystroke data should be encrypted at rest
5. **Access Control** - Restrict database access to authorized personnel

### Security Best Practices
```python
# Always use bcrypt for passwords
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Validate user input
if not username.isalnum() or len(username) < 3:
    raise ValueError("Invalid username")

# Use environment variables for sensitive config
WEBHOOK_URL = os.getenv('ZAPIER_WEBHOOK_URL')
```

## 📈 Machine Learning: Anomaly Detection

### Isolation Forest Algorithm
```python
from sklearn.ensemble import IsolationForest

# Train on baseline profile
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(baseline_features)

# Score new sample
anomaly_score = iso_forest.decision_function(current_features)
# Score < -0.2 = Anomaly detected!
```

### Threat Scoring
```
Typing Speed Analysis:
├── < 40 WPM  → Low suspicion
├── 40-70 WPM → Moderate suspicion
├── 70-100 WPM → High suspicion
└── > 100 WPM → Critical suspicion

Plus 7 additional metrics:
├── Key Latency (consistency of typing rhythm)
├── Hold Time (how long keys are pressed)
├── Flight Time (gaps between keystrokes)
├── Error Rate (backspace frequency)
├── Special Key Usage (modifier keys)
└── Overall typing speed pattern
```

## 🔔 Alert System

### Zapier Webhook Integration
```python
# Threat alerts sent via webhook
{
    "user_id": "john_doe",
    "reason": "Typing behavior anomaly detected."
}
```

**Response:** `200 OK` - Alert successfully logged

## 📊 Dashboard Walkthrough

### Login Page
```
1. Enter username
2. Enter password
3. Click "Login"
4. Redirected to appropriate dashboard (Admin/User)
```

### Admin Dashboard
```
1. View all users and their threat levels
2. See real-time activity visualization
3. Identify high-risk users
4. Take action on suspicious accounts
```

### User Dashboard
```
1. Type sample text
2. View real-time typing speed (WPM)
3. See suspicion level
4. View entertaining meme based on typing speed
```

## 🐛 Troubleshooting

### Keystroke Logger Not Working
```
Issue: "Permission denied" error
Solution: Run as administrator
          python keystroke_logger.py  # Windows: Run as Admin
          sudo python keystroke_logger.py  # Linux
```

### Profile Not Found
```
Issue: "User not found" message
Solution: User must register first using continuous_auth script
          Check typing_profiles/ folder for CSV files
```

### Dashboard Won't Start
```
Issue: Port 8501 already in use
Solution: streamlit run dashboard.py --server.port 8502
```

### Anomaly Detection Too Sensitive
```
Issue: False positives (legitimate users flagged)
Solution: Adjust ANOMALY_THRESHOLD
          Change from -0.2 to -0.15 (less strict)
```

## 🔍 Metrics Explained

| Metric | Unit | Description |
|--------|------|-------------|
| **Mean Hold Time** | seconds | Average duration a key is held |
| **Std Hold Time** | seconds | Consistency of key hold times |
| **Mean Flight Time** | seconds | Average gap between key presses |
| **Std Flight Time** | seconds | Consistency of gaps |
| **Key Latency** | seconds | Time between consecutive presses |
| **Typing Speed** | WPM | Words per minute |
| **Error Rate** | % | Percentage of backspace usage |
| **Special Key Usage** | count | Number of modifier keys used |

## 📚 Algorithm Flow

```
User Registration:
1. Collect 2 typing samples
2. Extract 8 metrics from each sample
3. Calculate averages
4. Store in CSV profile

User Verification:
1. Collect 2 typing samples
2. Extract 8 metrics
3. Normalize features (StandardScaler)
4. Compare with baseline using Isolation Forest
5. Generate anomaly score
6. If score < -0.2: Send alert via webhook
7. Display result to user
```

## 🔐 Password Security

```python
# Registration
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Verification
bcrypt.checkpw(password.encode(), hashed.encode())
```

## 📤 Zapier Integration

### Setup Webhook:
1. Go to Zapier.com
2. Create new Zap
3. Trigger: Webhooks by Zapier → "Catch Hook"
4. Get webhook URL
5. Add to script: `ZAPIER_WEBHOOK_URL = "your_url"`

### Example Alert Action:
- Send email to security team
- Create Slack message
- Log to security database
- Create ticket in Jira

## 🎓 Use Cases

1. **Enterprise Security** - Monitor employees for data theft
2. **Sensitive Access Control** - Verify user identity continuously
3. **Fraud Detection** - Identify account takeovers
4. **Behavioral Analytics** - Understand typing patterns
5. **Access Logging** - Audit trail of who typed what

## ⚙️ Configuration Reference

```python
# continuous_auth (5).py
DATA_DIR = "typing_profiles"           # Profile storage location
SAMPLE_TEXT = "The quick brown fox..." # Registration text

# typing_auth (2).py
ANOMEALY_THRESHOLD = -0.2              # Detection sensitivity
NUM_SAMPLES = 2                        # Samples per verification
ZAPIER_WEBHOOK_URL = "https://..."    # Alert endpoint

# keystroke_logger (2).py
log_file = r"C:\Users\...\k.csv"      # Log file path

# dashboard.py
DB_PATH = "users.db"                  # SQLite database
```

## 📝 Example Workflow

```bash
# 1. Register John Doe
$ python "continuous_auth (5).py"
Enter new username: john_doe
[Type sample text twice]

# 2. Verify John's typing
$ python "typing_auth (2).py"
Choose (1=Register, 2=Verify): 2
Enter username: john_doe
[Type verification text]
→ "No anomaly detected. It's you."

# 3. Launch dashboard
$ streamlit run dashboard.py
→ http://localhost:8501

# 4. Log in as admin
Username: admin
Password: admin123
→ View threat dashboard
```

## 📊 Sample Output

```
Anomaly Score: -0.1523
Typing Speed: 72.34 WPM
Error Rate: 3.2%
Mean Hold Time: 0.0523 sec
Mean Flight Time: 0.0891 sec
Special Key Usage: 5

→ Status: ✅ Verified User
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Make changes and test thoroughly
4. Commit (`git commit -m 'Add improvement'`)
5. Push (`git push origin feature/improvement`)
6. Create Pull Request

## 📜 License

[Add appropriate license]

## ⚖️ Disclaimer

This system is designed for **authorized security monitoring only**. Ensure compliance with:
- Local employment laws
- Data protection regulations (GDPR, CCPA, etc.)
- Workplace privacy policies
- Written consent from monitored users

## 🔗 Resources

- [pynput Documentation](https://pynput.readthedocs.io/)
- [scikit-learn Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Keystroke Dynamics Research](https://en.wikipedia.org/wiki/Keystroke_dynamics)

## 📞 Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Email: support@example.com
- Documentation: [Full Docs](./docs)

---

**Last Updated:** October 2025  
**Language:** Python 100%  
**Status:** Active Development  
**Maintainer:** Jananisri05