
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
    window.geometry("450x450")
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

    book_list = tk.Listbox(
        window,
        width=40,
        height=12,
        font=("Arial", 12),
        bg="white",
        fg=TEXT_COLOR
    )
    book_list.pack(pady=10)

    for book in books:
        book_list.insert(
            tk.END,
            f"{book['title']} - {book['author']}"
        )

    tk.Label(
        window,
        text="Choose a rating from 1 to 5",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=5)

    rating = tk.IntVar(value=5)

    tk.Scale(
        window,
        from_=1,
        to=5,
        orient="horizontal",
        variable=rating,
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_COLOR
    ).pack()

    def save_rating():
        selection = book_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Select a Book",
                "Please select a book to rate.",
                parent=window
            )
            return

        index = selection[0]
        books[index]["rating"] = rating.get()

        save_books(books)

        messagebox.showinfo(
            "Rating Saved",
            "Your rating was saved!",
            parent=window
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
    ).pack(pady=15)

    return window
