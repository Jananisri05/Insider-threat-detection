from pynput import keyboard
import time
import csv
import os

import os as _os
log_file = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "k.csv")  # Path to save logs

# Ensure file and header exist
if not os.path.exists(log_file):
    try:
        with open(log_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["key_str", "human_time", "epoch_time", "hold_seconds"])
    except Exception as e:
        print(f"Error creating log file: {e}")
        raise

press_times = {}  # Store key press epoch times, keyed by key string

def key_to_str(key):
    """
    Convert a pynput Key or KeyCode to a readable string.
    Examples:
      - letter keys -> 'a'
      - space -> 'Key.space' (you can convert to ' ' if desired)
    """
    try:
        # Key.char exists for normal character keys
        return key.char
    except AttributeError:
        # Special keys (space, ctrl, esc) become strings like 'Key.space'
        return str(key)

def on_press(key):
    """Called when a key is pressed."""
    kstr = key_to_str(key)
    press_times[kstr] = time.time()
    # Optional feedback:
    print(f"Pressed: {kstr}")

def on_release(key):
    """Called when a key is released."""
    kstr = key_to_str(key)
    press_time = press_times.pop(kstr, None)  # remove to avoid growth
    
    if press_time:
        hold_time = time.time() - press_time  # seconds
        human_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        epoch_time = time.time()

        # Debug output
        print(f"Released: {kstr}, Hold Time: {hold_time:.3f} sec")

        # Save to CSV
        try:
            with open(log_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([kstr, human_time, f"{epoch_time:.6f}", f"{hold_time:.6f}"])
        except Exception as e:
            print(f"Error writing to file: {e}")

    # Stop logging when Esc key is pressed
    # Note: for special key objects, key_to_str returns 'Key.esc'
    if kstr in ("Key.esc", "esc"):
        print("Exiting...")
        return False

# Start key listener
print(f"Keystroke logger is running... logging to: {log_file}")
print("Press keys; press ESC to stop.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
