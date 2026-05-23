import json, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "edr_logs.json")
OUTPUT = os.path.join(os.path.dirname(__file__), "EDR_Report.pdf")

def generate_report():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    c = canvas.Canvas(OUTPUT, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, h - 60, "EDR Honeypot Security Report")
    c.setFont("Helvetica", 11)
    c.drawString(50, h - 85, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, h - 100, f"Total Events: {len(logs)}")

    c.setFont("Helvetica-Bold", 10)
    y = h - 130
    c.drawString(50, y, "Time"); c.drawString(110, y, "Level")
    c.drawString(200, y, "Event"); c.drawString(370, y, "Details")
    y -= 15
    c.line(50, y, w - 50, y)

    c.setFont("Helvetica", 9)
    for log in reversed(logs):
        y -= 18
        if y < 60:
            c.showPage()
            y = h - 60
            c.setFont("Helvetica", 9)
        c.drawString(50, y, log.get("time", ""))
        c.drawString(110, y, log.get("level", ""))
        c.drawString(200, y, log.get("event", "")[:20])
        c.drawString(370, y, log.get("details", "")[:30])

    c.save()
    print(f"[+] Report saved to {OUTPUT}")
    return OUTPUT