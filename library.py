import tkinter as tk

from book_data import load_books


BG_COLOR = "#CAD2C5"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_library(parent):
    window = tk.Toplevel(parent)
    window.title("My Library")
    window.geometry("500x500")
    window.configure(bg=BG_COLOR)

    title = tk.Label(
        window,
        text="My Library",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    )
    title.pack(pady=20)

    books = load_books()

    book_list = tk.Listbox(
        window,
        width=45,
        height=18,
        font=("Arial", 12),
        bg="white",
        fg=TEXT_COLOR
    )
    book_list.pack(pady=10)

    if not books:
        book_list.insert(tk.END, "Your library is empty.")

    for book in books:
        book_list.insert(
            tk.END,
            f"{book['title']} by {book['author']}"
        )

    return window