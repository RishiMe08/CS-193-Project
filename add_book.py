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
    window.geometry("450x500")
    window.configure(bg=BG_COLOR)

    title = tk.Label(
        window,
        text="Add a Book",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    )
    title.pack(pady=20)

    tk.Label(
        window,
        text="Book Title",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    title_entry = tk.Entry(window, width=35, font=("Arial", 12))
    title_entry.pack(pady=5)

    tk.Label(
        window,
        text="Author",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    author_entry = tk.Entry(window, width=35, font=("Arial", 12))
    author_entry.pack(pady=5)

    tk.Label(
        window,
        text="Genre",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    genre_entry = tk.Entry(window, width=35, font=("Arial", 12))
    genre_entry.pack(pady=5)

    tk.Label(
        window,
        text="Reading Status",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    status = tk.StringVar(value="Want to Read")

    status_menu = tk.OptionMenu(
        window,
        status,
        "Read",
        "Currently Reading",
        "Want to Read"
    )
    status_menu.pack(pady=5)

    def save_book():
        book_title = title_entry.get().strip()
        author = author_entry.get().strip()
        genre = genre_entry.get().strip()

        if not book_title or not author:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the book title and author."
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
            "Your book was saved to your library."
        )

        window.destroy()

    save_button = tk.Button(
        window,
        text="Save Book",
        command=save_book,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=20
    )
    save_button.pack(pady=20)

    return window