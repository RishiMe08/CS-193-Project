
import tkinter as tk
from tkinter import messagebox

from book_data import add_book


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_add_book(parent):
    window = tk.Toplevel(parent)
    window.title("Add Book")
    window.geometry("450x550")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="Add a Book",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    tk.Label(
        window,
        text="Book Title",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    title_entry = tk.Entry(window, width=35, font=("Arial", 12))
    title_entry.pack(pady=5)

    tk.Label(
        window,
        text="Author",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    author_entry = tk.Entry(window, width=35, font=("Arial", 12))
    author_entry.pack(pady=5)

    tk.Label(
        window,
        text="Genre",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    genre_entry = tk.Entry(window, width=35, font=("Arial", 12))
    genre_entry.pack(pady=5)

    tk.Label(
        window,
        text="Reading Status",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    status = tk.StringVar(value="Want to Read")

    tk.OptionMenu(
        window,
        status,
        "Read",
        "Currently Reading",
        "Want to Read"
    ).pack(pady=5)

    def save_new_book():
        book_title = title_entry.get().strip()
        author = author_entry.get().strip()
        genre = genre_entry.get().strip()

        if not book_title or not author:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the title and author.",
                parent=window
            )
            return

        book = {
            "title": book_title,
            "author": author,
            "genre": genre,
            "status": status.get(),
            "rating": 0
        }

        add_book(book)

        messagebox.showinfo(
            "Book Added",
            "Your book was saved!",
            parent=window
        )

        window.destroy()

    tk.Button(
        window,
        text="Save Book",
        command=save_new_book,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=20
    ).pack(pady=25)

    return window
