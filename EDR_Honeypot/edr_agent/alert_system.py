import json, os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "edr_logs.json")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "logs", "screenshots")

def take_screenshot(event_type):
    try:
        import pyautogui
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{event_type}_{timestamp}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print(f"[📸] Screenshot saved: {filename}")
        return filename
    except Exception as e:
        print(f"[!] Screenshot failed: {e}")
        return None

def log_event(level, event_type, details, notify=False):
    screenshot_file = None

    # Auto screenshot on any CRITICAL honeypot event
    if level == "CRITICAL" and "HONEYPOT" in event_type:
        screenshot_file = take_screenshot(event_type)

    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "level": level,
        "event": event_type,
        "details": details,
        "screenshot": screenshot_file
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"[{level}] {event_type} | {details}")

    if notify:
        try:
            from plyer import notification
            notification.notify(
                title=f"EDR ALERT: {level}",
                message=f"{event_type} — {details}",
                timeout=5
            )
        except:
            pass