
import tkinter as tk
from tkinter import ttk, messagebox

from book_data import add_book
from genres import GENRES


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_add_book(parent):
    window = tk.Toplevel(parent)
    window.title("BookMatch - Add Book")
    window.geometry("450x550")
    window.configure(bg=BG_COLOR)

    heading = tk.Label(
        window,
        text="Add a Book",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    )
    heading.pack(pady=20)

    title_label = tk.Label(
        window,
        text="Book Title:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=5)

    title_entry = tk.Entry(
        window,
        font=("Arial", 12),
        width=30
    )
    title_entry.pack(pady=5)

    author_label = tk.Label(
        window,
        text="Author:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    author_label.pack(pady=5)

    author_entry = tk.Entry(
        window,
        font=("Arial", 12),
        width=30
    )
    author_entry.pack(pady=5)

    genre_label = tk.Label(
        window,
        text="Genre:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    genre_label.pack(pady=5)

    genre_menu = ttk.Combobox(
        window,
        values=GENRES,
        state="readonly",
        font=("Arial", 12),
        width=27
    )
    genre_menu.pack(pady=5)
    genre_menu.set("Choose a genre")

    status_label = tk.Label(
        window,
        text="Reading Status:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    status_label.pack(pady=5)

    status_options = [
        "Read",
        "Currently Reading",
        "Want to Read"
    ]

    status_variable = tk.StringVar(
        value="Want to Read"
    )

    status_menu = tk.OptionMenu(
        window,
        status_variable,
        *status_options
    )
    status_menu.config(
        font=("Arial", 11),
        bg=BUTTON_COLOR,
        fg=HEADING_COLOR
    )
    status_menu.pack(pady=5)

    def save_book():
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        genre = genre_menu.get()
        status = status_variable.get()

        if not title:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the book title."
            )
            return

        if not author:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the author."
            )
            return

        if genre not in GENRES:
            messagebox.showwarning(
                "Missing Information",
                "Please choose a genre."
            )
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "status": status,
            "rating": 0
        }

        add_book(book)

        messagebox.showinfo(
            "Book Added",
            f"{title} was added to your library."
        )

        window.destroy()

    save_button = tk.Button(
        window,
        text="Save Book",
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=HEADING_COLOR,
        command=save_book
    )
    save_button.pack(pady=20)

    close_button = tk.Button(
        window,
        text="Cancel",
        font=("Arial", 12),
        bg="#52796F",
        fg="white",
        command=window.destroy
    )
    close_button.pack(pady=5)
