import tkinter as tk
from tkinter import messagebox

CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "edr@1234"

def show_login(on_success):
    login = tk.Tk()
    login.title("EDR System Login")
    login.geometry("400x300")
    login.configure(bg="#1a1a2e")
    login.resizable(False, False)

    tk.Label(login, text="🛡️ EDR HONEYPOT SYSTEM",
             font=("Courier", 14, "bold"),
             bg="#1a1a2e", fg="#00ff88").pack(pady=20)

    tk.Label(login, text="Authorized Access Only",
             font=("Courier", 9),
             bg="#1a1a2e", fg="#ff4444").pack()

    tk.Label(login, text="Username",
             font=("Courier", 10),
             bg="#1a1a2e", fg="white").pack(pady=(20, 5))

    username_var = tk.StringVar()
    username_entry = tk.Entry(login, textvariable=username_var,
                              font=("Courier", 11), width=25,
                              bg="#16213e", fg="white",
                              insertbackground="white")
    username_entry.pack()
    username_entry.focus()

    tk.Label(login, text="Password",
             font=("Courier", 10),
             bg="#1a1a2e", fg="white").pack(pady=(10, 5))

    password_var = tk.StringVar()
    password_entry = tk.Entry(login, textvariable=password_var,
                              font=("Courier", 11), width=25,
                              show="*", bg="#16213e", fg="white",
                              insertbackground="white")
    password_entry.pack()

    attempts = [0]

    def try_login(event=None):
        username = username_var.get()
        password = password_var.get()

        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            login.destroy()
            on_success()
        else:
            attempts[0] += 1
            remaining = 3 - attempts[0]
            if remaining <= 0:
                messagebox.showerror("ACCESS DENIED",
                                     "Too many failed attempts!\nSystem locked.")
                login.destroy()
            else:
                messagebox.showwarning("ACCESS DENIED",
                                       f"Wrong credentials!\n{remaining} attempts remaining.")
                password_var.set("")

    password_entry.bind("<Return>", try_login)

    tk.Button(login, text="LOGIN",
              command=try_login,
              font=("Courier", 11, "bold"),
              bg="#00ff88", fg="#1a1a2e",
              width=20, cursor="hand2").pack(pady=20)

    tk.Label(login, text="Default: admin / edr@1234",
             font=("Courier", 8),
             bg="#1a1a2e", fg="#555555").pack()

    login.mainloop()