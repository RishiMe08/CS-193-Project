import tkinter as tk


BG_COLOR = "#CAD2C5"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_find_books(parent):
    window = tk.Toplevel(parent)
    window.title("Find New Books")
    window.geometry("500x400")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="Find New Books",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    tk.Label(
        window,
        text="Search for books you might want to read.",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    search_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )
    search_entry.pack(pady=10)

    tk.Label(
        window,
        text="Online book search will be added in a later milestone.",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        wraplength=400
    ).pack(pady=20)

    return window