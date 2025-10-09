import os
import csv
import time
import numpy as np
from pynput import keyboard

DATA_DIR = "typing_profiles"
SAMPLE_TEXT = "The quick brown fox jumps over the lazy dog"

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

def calculate_typing_profile(events, press_times):
    """Extract hold and flight times from key events."""
    hold_times = []
    flight_times = []
    last_release_time = None

    for event in events:
        action, key, timestamp = event
        if action == "press":
            if last_release_time:
                flight_times.append(timestamp - last_release_time)
            press_times[key] = timestamp
        elif action == "release":
            if key in press_times:
                hold_times.append(timestamp - press_times[key])
                last_release_time = timestamp

    return {
        "mean_hold_time": np.mean(hold_times) if hold_times else 0,
        "std_hold_time": np.std(hold_times) if hold_times else 0,
        "mean_flight_time": np.mean(flight_times) if flight_times else 0,
        "std_flight_time": np.std(flight_times) if flight_times else 0,
    }

def register_user(username):
    """Registers a new user by collecting typing samples."""
    profile_path = os.path.join(DATA_DIR, f"{username}.csv")

    print(f"\n🔹 Registration for user: {username}")
    print(f"Please type the following text exactly as shown:")
    print(f"\n👉 {SAMPLE_TEXT}\n")

    all_profiles = []
    for i in range(2):  # Two samples
        print(f"Sample {i + 1}/2 — start typing now (press Esc when done)...")

        events = []
        press_times = {}

        def on_press(key):
            events.append(("press", key, time.time()))

        def on_release(key):
            events.append(("release", key, time.time()))
            if key == keyboard.Key.esc:
                return False

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        profile = calculate_typing_profile(events, press_times)
        all_profiles.append(profile)
        print(f"✅ Sample {i + 1} recorded.\n")

    # Compute average profile across both samples
    avg_profile = {
        "mean_hold_time": np.mean([p["mean_hold_time"] for p in all_profiles]),
        "std_hold_time": np.mean([p["std_hold_time"] for p in all_profiles]),
        "mean_flight_time": np.mean([p["mean_flight_time"] for p in all_profiles]),
        "std_flight_time": np.mean([p["std_flight_time"] for p in all_profiles]),
    }

    # Save profile
    with open(profile_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, val in avg_profile.items():
            writer.writerow([key, val])

    print(f"🎉 Registration complete for {username}. Profile saved at {profile_path}\n")

# Run registration if script executed directly
if __name__ == "__main__":
    username = input("Enter new username: ")
    register_user(username)
