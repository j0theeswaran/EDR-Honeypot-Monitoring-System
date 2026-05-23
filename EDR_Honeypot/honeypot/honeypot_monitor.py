import os, sys, time, threading
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from edr_agent.alert_system import log_event

HONEYPOT_DIR = os.path.join(os.path.dirname(__file__), "fake_files")

def get_file_times():
    times = {}
    for f in os.listdir(HONEYPOT_DIR):
        path = os.path.join(HONEYPOT_DIR, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            times[f] = {
                "modified": stat.st_mtime,
                "accessed": stat.st_atime,
                "size": stat.st_size
            }
    return times

def monitor_loop():
    log_event("INFO", "EDR STARTED", "Honeypot monitor active", notify=False)
    previous = get_file_times()

    while True:
        time.sleep(2)
        current = get_file_times()

        for filename in current:
            if filename not in previous:
                log_event("CRITICAL", "NEW FILE IN HONEYPOT", filename, notify=True)
                continue

            prev = previous[filename]
            curr = current[filename]

            # File was VIEWED — access time changed but not modified
            if curr["accessed"] != prev["accessed"] and curr["modified"] == prev["modified"]:
                log_event("CRITICAL", "HONEYPOT VIEWED", filename, notify=True)

            # File was MODIFIED
            elif curr["modified"] != prev["modified"]:
                log_event("CRITICAL", "HONEYPOT MODIFIED", filename, notify=True)

        # File was DELETED
        for filename in previous:
            if filename not in current:
                log_event("CRITICAL", "HONEYPOT DELETED", filename, notify=True)

        previous = current

def start_honeypot_monitor(path=None):
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()

    class FakeObserver:
        def stop(self): pass
        def join(self): pass

    return FakeObserver()