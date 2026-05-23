import os

def create_honeypot_files():
    base = os.path.join(os.path.dirname(__file__), "fake_files")
    os.makedirs(base, exist_ok=True)

    files = {
        "passwords.txt": "admin:Admin@1234\nroot:Root#9876\nceo_login:Ceo$Pass2024",
        "bank_details.txt": "Account: 9876543210\nIFSC: HDFC0001234\nBalance: Rs.14,50,000",
        "confidential.txt": "Project X Launch: March 2025\nBudget: 50 Crore INR\nPartner: TCS",
        "employee_data.txt": "Amit Sharma | Sr. Dev | Salary: 18LPA\nPriya Singh | Manager | Salary: 24LPA",
    }

    for filename, content in files.items():
        path = os.path.join(base, filename)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content)
    print("[+] Honeypot files created.")