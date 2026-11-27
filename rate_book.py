import tkinter as tk
from tkinter import messagebox

from book_data import load_books, save_books


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_rate_book(parent):
    window = tk.Toplevel(parent)
    window.title("Rate Book")
    window.geometry("450x400")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="Rate a Book",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    books = load_books()

    if not books:
        tk.Label(
            window,
            text="Add a book to your library first.",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)

        return window

    book_names = [
        f"{book['title']} by {book['author']}"
        for book in books
    ]

    selected_book = tk.StringVar(value=book_names[0])

    tk.Label(
        window,
        text="Select a Book",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    tk.OptionMenu(
        window,
        selected_book,
        *book_names
    ).pack(pady=10)

    rating = tk.IntVar(value=5)

    tk.Label(
        window,
        text="Rating (1-5)",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    tk.Scale(
        window,
        from_=1,
        to=5,
        orient="horizontal",
        variable=rating,
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    def save_rating():
        index = book_names.index(selected_book.get())

        books[index]["rating"] = rating.get()

        save_books(books)

        messagebox.showinfo(
            "Rating Saved",
            "Your rating has been saved."
        )

        window.destroy()

    tk.Button(
        window,
        text="Save Rating",
        command=save_rating,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=20
    ).pack(pady=20)

    return window