import os
import csv
import ast
import time
import requests
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from pynput import keyboard

# Configuration
DATA_DIR = "typing_profiles"
SAMPLE_TEXTS = [
    "Unicorns dance on rainbows!",
    "Dragons love marshmallow clouds."
]
VERIFICATION_TEXT = "Unicorns dance on rainbows!"
NUM_SAMPLES = 2
ANOMALY_THRESHOLD = -0.2
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21984357/2ql594u/"

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def log_threat(user_id, reason):
    """Logs detected threats and sends alerts via Zapier Webhook."""
    data = {"user_id": user_id, "reason": reason}

    try:
        response = requests.post(ZAPIER_WEBHOOK_URL, json=data)
        print(f"Zapier Response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print(f"Failed to send alert: {response.text}")
    except Exception as e:
        print(f"Error sending alert: {e}")


def calculate_typing_profile(events):
    """Calculate typing profile from key events."""
    press_times = {}
    hold_times = {}
    flight_times = {}
    key_latencies = []
    backspace_count = 0
    total_keys_pressed = 0
    special_key_count = 0
    last_release_time = None
    last_press_time = None
    last_key = None

    for event in events:
        action, key, timestamp = event

        if action == "press":
            total_keys_pressed += 1
            if last_release_time:
                flight_time = timestamp - last_release_time
                if last_key:
                    key_pair = (str(last_key), str(key))
                    flight_times[key_pair] = flight_times.get(key_pair, []) + [flight_time]

            if last_press_time:
                key_latencies.append(timestamp - last_press_time)

            press_times[key] = timestamp
            last_press_time = timestamp

            if key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.alt):
                special_key_count += 1

        elif action == "release":
            if key in press_times:
                hold_time = timestamp - press_times[key]
                hold_times[str(key)] = hold_times.get(str(key), []) + [hold_time]
                last_release_time = timestamp
                last_key = key

            if key == keyboard.Key.backspace:
                backspace_count += 1

    if not events:
        return {}

    per_key_hold_times = {str(k): np.mean(v) for k, v in hold_times.items() if v}
    per_key_flight_times = {str(k): np.mean(v) for k, v in flight_times.items() if v}
    typing_speed = total_keys_pressed / (last_release_time - events[0][2]) if last_release_time else 0
    error_rate = backspace_count / total_keys_pressed if total_keys_pressed > 0 else 0

    return {
        "mean_key_latency": np.mean(key_latencies) if key_latencies else 0,
        "std_key_latency": np.std(key_latencies) if key_latencies else 0,
        "error_rate": error_rate,
        "special_key_usage": special_key_count,
        "typing_speed": typing_speed,
        "mean_hold_time": np.mean(list(per_key_hold_times.values())) if per_key_hold_times else 0,
        "mean_flight_time": np.mean(list(per_key_flight_times.values())) if per_key_flight_times else 0
    }


def verify_user(username):
    """Verify a user by comparing their typing behavior with the stored profile."""
    profile_path = os.path.join(DATA_DIR, f"{username}.csv")
    if not os.path.exists(profile_path):
        print("User not found. Please register first.")
        return

    stored_profile = {}
    with open(profile_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == 2:
                stored_profile[row[0]] = float(row[1]) if row[1].replace('.', '', 1).isdigit() else 0.0

    if not stored_profile:
        print("Error: No valid stored profile found.")
        return

    print("\nVerification: Please type the following text twice.")
    events = collect_typing_samples(VERIFICATION_TEXT, NUM_SAMPLES)
    current_profile = calculate_typing_profile(events)

    feature_keys = list(stored_profile.keys())
    stored_values = np.array([stored_profile.get(k, 0) for k in feature_keys]).reshape(1, -1)
    current_values = np.array([current_profile.get(k, 0) for k in feature_keys]).reshape(1, -1)

    scaler = StandardScaler()
    combined = np.vstack([stored_values, current_values])
    combined_scaled = scaler.fit_transform(combined)

    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    iso_forest.fit(combined_scaled[:1])

    anomaly_score = iso_forest.decision_function(combined_scaled[1:])[0]
    print(f"Anomaly Score: {anomaly_score:.4f}")

    if anomaly_score < ANOMALY_THRESHOLD:
        print("Anomaly detected! This might not be you.")
        log_threat(username, "Typing behavior anomaly detected.")
    else:
        print("No anomaly detected. It's you.")


def collect_typing_samples(sample_text, num_samples):
    """Collect typing samples from the user."""
    all_events = []

    for sample_num in range(num_samples):
        print(f"\nSample {sample_num + 1} of {num_samples}:")
        print(f"Type this exactly: {sample_text}")
        print("(Press ESC when finished typing.)")

        events = []

        def on_press(key):
            events.append(("press", key, time.time()))

        def on_release(key):
            events.append(("release", key, time.time()))
            if key == keyboard.Key.esc:
                return False

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        all_events.extend(events)

    return all_events


def register_user(username):
    """Register a new user by capturing their typing behavior."""
    print("Registration: Please type the following texts twice.")
    all_events = []

    for text in SAMPLE_TEXTS:
        events = collect_typing_samples(text, NUM_SAMPLES)
        all_events.extend(events)

    profile = calculate_typing_profile(all_events)
    profile_path = os.path.join(DATA_DIR, f"{username}.csv")

    with open(profile_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for metric, value in profile.items():
            writer.writerow([metric, value])

    print(f"Registration complete. Profile saved to {profile_path}")


def main():
    """Main function to handle registration and verification."""
    print("1. Register\n2. Verify")
    choice = input("Choose an option (1 or 2): ")

    username = input("Enter your username: ").strip()

    if choice == "1":
        register_user(username)
    elif choice == "2":
        verify_user(username)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
