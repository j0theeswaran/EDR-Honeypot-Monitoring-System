import psutil
import threading, time
from edr_agent.alert_system import log_event

SUSPICIOUS = ["netcat", "nmap", "mimikatz", "wireshark", "metasploit"]

WHITELIST = ["system idle process", "system", "registry", "smss.exe",
             "csrss.exe", "wininit.exe", "services.exe", "lsass.exe",
             "svchost.exe", "dwm.exe", "explorer.exe"]

def monitor_processes():
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'status']):
            try:
                name = proc.info['name'].lower()
                cpu = proc.info['cpu_percent']

                if name in WHITELIST:
                    continue

                # Notify for suspicious process — real threat
                if any(s in name for s in SUSPICIOUS):
                    log_event("CRITICAL", "SUSPICIOUS PROCESS",
                              f"{proc.info['name']} PID:{proc.info['pid']}",
                              notify=True)

                # Log high CPU — no notification
                elif cpu and cpu > 90:
                    log_event("WARNING", "HIGH CPU PROCESS",
                              f"{proc.info['name']} CPU:{cpu}%",
                              notify=False)

                # Log all normal processes silently
                else:
                    log_event("INFO", "PROCESS RUNNING",
                              f"{proc.info['name']} PID:{proc.info['pid']}",
                              notify=False)

            except:
                pass
        time.sleep(15)

def start_process_monitor():
    t = threading.Thread(target=monitor_processes, daemon=True)
    t.start()