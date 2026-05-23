import tkinter as tk
from tkinter import ttk
import json, os, threading
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "edr_logs.json")

def read_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def launch_dashboard():
    root = tk.Tk()
    root.title("EDR Honeypot Monitoring System")
    root.geometry("900x600")
    root.configure(bg="#1a1a2e")

    tk.Label(root, text="EDR HONEYPOT MONITORING SYSTEM", font=("Courier", 16, "bold"),
             bg="#1a1a2e", fg="#00ff88").pack(pady=10)

    stats_frame = tk.Frame(root, bg="#1a1a2e")
    stats_frame.pack(fill="x", padx=20)

    total_var = tk.StringVar(value="Total: 0")
    crit_var  = tk.StringVar(value="Critical: 0")
    warn_var  = tk.StringVar(value="Warning: 0")
    info_var  = tk.StringVar(value="Info: 0")

    for var, color in [(total_var,"#ffffff"),(crit_var,"#ff4444"),(warn_var,"#ff9900"),(info_var,"#44ff88")]:
        tk.Label(stats_frame, textvariable=var, font=("Courier", 12, "bold"),
                 bg="#1a1a2e", fg=color).pack(side="left", padx=20)

    cols = ("Time", "Level", "Event", "Details")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=20)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    style = ttk.Style()
    style.configure("Treeview", background="#16213e", foreground="white",
                    fieldbackground="#16213e", font=("Courier", 10))
    style.configure("Treeview.Heading", background="#0f3460", foreground="white",
                    font=("Courier", 10, "bold"))

    tree.tag_configure("CRITICAL", background="#3d0000")
    tree.tag_configure("WARNING",  background="#2d1a00")
    tree.tag_configure("INFO",     background="#001a2d")

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    status_var = tk.StringVar(value="System Active | Monitoring...")
    tk.Label(root, textvariable=status_var, font=("Courier", 10),
             bg="#1a1a2e", fg="#00ff88").pack(pady=5)

    def refresh():
        logs = read_logs()
        tree.delete(*tree.get_children())
        crit = warn = info = 0
        for log in reversed(logs):
            lvl = log.get("level","INFO")
            if lvl == "CRITICAL": crit += 1
            elif lvl == "WARNING": warn += 1
            else: info += 1
            tree.insert("", "end",
                values=(log.get("time",""), lvl, log.get("event",""), log.get("details","")),
                tags=(lvl,))
        total_var.set(f"Total: {len(logs)}")
        crit_var.set(f"Critical: {crit}")
        warn_var.set(f"Warning: {warn}")
        info_var.set(f"Info: {info}")
        root.after(3000, refresh)

    def clear_logs():
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
        refresh()

    def gen_report():
        from reports.report_generator import generate_report
        path = generate_report()
        status_var.set(f"Report saved: {path}")
        os.startfile(path)

    btn_frame = tk.Frame(root, bg="#1a1a2e")
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Refresh",        command=refresh,    bg="#0f3460", fg="white", font=("Courier",10)).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Clear Logs",     command=clear_logs, bg="#3d0000", fg="white", font=("Courier",10)).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Generate Report",command=gen_report, bg="#1a3d00", fg="white", font=("Courier",10)).pack(side="left", padx=8)

    refresh()
    root.mainloop()