
import tkinter as tk
from tkinter import messagebox

from user_data import create_account, login_user


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_login(parent, on_login):
    window = tk.Frame(parent, bg=BG_COLOR)
    window.pack(fill="both", expand=True)

    tk.Label(
        window,
        text="BookMatch",
        font=("Arial", 32, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=(60, 5))

    tk.Label(
        window,
        text="Your personal reading companion",
        font=("Arial", 14),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(0, 30))

    tk.Label(
        window,
        text="Username",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    username_entry = tk.Entry(window, width=30, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(
        window,
        text="Password",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    password_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12),
        show="*"
    )
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get()

        success, message = login_user(username, password)

        if success:
            window.destroy()
            on_login()
        else:
            messagebox.showwarning(
                "Login Failed",
                message,
                parent=parent
            )

    def register():
        username = username_entry.get().strip()
        password = password_entry.get()

        if len(password) < 8:
            messagebox.showwarning(
                "Password Too Short",
                "Use a password with at least 8 characters.",
                parent=parent
            )
            return

        success, message = create_account(username, password)

        if success:
            success, login_message = login_user(username, password)

            if success:
                window.destroy()
                on_login()
        else:
            messagebox.showwarning(
                "Account Creation",
                message,
                parent=parent
            )

    tk.Button(
        window,
        text="Log In",
        command=login,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=22
    ).pack(pady=(25, 8))

    tk.Button(
        window,
        text="Create Account",
        command=register,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=22
    ).pack(pady=8)

    return window
