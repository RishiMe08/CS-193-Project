
import tkinter as tk

from book_data import load_books


BG_COLOR = "#CAD2C5"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_library(parent):
    window = tk.Toplevel(parent)
    window.title("My Library")
    window.geometry("550x550")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="My Library",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    books = load_books()

    book_list = tk.Listbox(
        window,
        width=50,
        height=20,
        font=("Arial", 12),
        bg="white",
        fg=TEXT_COLOR
    )
    book_list.pack(pady=10)

    if not books:
        book_list.insert(tk.END, "Your library is empty.")
    else:
        for book in books:
            book_list.insert(
                tk.END,
                f"{book['title']} - {book['author']}"
            )

    details = tk.Label(
        window,
        text="Select a book to see its details.",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    details.pack(pady=10)

    def show_details(event):
        selection = book_list.curselection()

        if not selection or not books:
            return

        index = selection[0]
        book = books[index]

        rating = book.get("rating", 0)

        if rating == 0:
            rating_text = "Not rated"
        else:
            rating_text = f"{rating}/5"

        details.config(
            text=(
                f"Genre: {book.get('genre', '')}\n"
                f"Status: {book.get('status', '')}\n"
                f"Rating: {rating_text}"
            )
        )

    book_list.bind("<<ListboxSelect>>", show_details)

    return window
