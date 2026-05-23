import os, sys, threading

sys.path.insert(0, os.path.dirname(__file__))

from honeypot.honeypot_setup import create_honeypot_files
from honeypot.honeypot_monitor import start_honeypot_monitor
from edr_agent.process_monitor import start_process_monitor
from dashboard.login import show_login
from dashboard.main_dashboard import launch_dashboard

if __name__ == "__main__":
    print("[*] Starting EDR Honeypot System...")

    create_honeypot_files()

    honeypot_path = os.path.join(os.path.dirname(__file__), "honeypot", "fake_files")
    observer = start_honeypot_monitor(honeypot_path)

    start_process_monitor()

    print("[*] Launching Login...")
    show_login(on_success=launch_dashboard)

    observer.stop()
    observer.join()