
import tkinter as tk
from tkinter import messagebox

from book_data import load_books


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_search_books(parent):
    window = tk.Toplevel(parent)
    window.title("BookMatch - Search Books")
    window.geometry("650x500")
    window.configure(bg=BG_COLOR)

    heading = tk.Label(
        window,
        text="Search Your Library",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    )
    heading.pack(pady=20)

    search_label = tk.Label(
        window,
        text="Enter a book title or author:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    search_label.pack(pady=5)

    search_entry = tk.Entry(
        window,
        font=("Arial", 13),
        width=35
    )
    search_entry.pack(pady=10)

    result_frame = tk.Frame(window, bg=BG_COLOR)
    result_frame.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(
        result_frame,
        bg=BG_COLOR,
        highlightthickness=0
    )
    scrollbar = tk.Scrollbar(
        result_frame,
        orient="vertical",
        command=canvas.yview
    )

    results_frame = tk.Frame(canvas, bg=BG_COLOR)

    results_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=results_frame,
        anchor="nw"
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def search():
        search_text = search_entry.get().strip().lower()

        for widget in results_frame.winfo_children():
            widget.destroy()

        if not search_text:
            messagebox.showwarning(
                "Search",
                "Please enter a book title or author."
            )
            return

        books = load_books()
        matches = []

        for book in books:
            title = book.get("title", "").lower()
            author = book.get("author", "").lower()

            if search_text in title or search_text in author:
                matches.append(book)

        if not matches:
            no_results = tk.Label(
                results_frame,
                text="No matching books found in your library.",
                font=("Arial", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            )
            no_results.pack(pady=20)
            return

        for book in matches:
            title = book.get("title", "Unknown title")
            author = book.get("author", "Unknown author")
            rating = book.get("rating", "Not rated")

            card = tk.Frame(
                results_frame,
                bg=BUTTON_COLOR,
                padx=12,
                pady=10
            )
            card.pack(fill="x", pady=6)

            title_label = tk.Label(
                card,
                text=title,
                font=("Arial", 14, "bold"),
                bg=BUTTON_COLOR,
                fg=HEADING_COLOR,
                wraplength=500,
                justify="left"
            )
            title_label.pack(anchor="w")

            author_label = tk.Label(
                card,
                text=f"Author: {author}",
                font=("Arial", 11),
                bg=BUTTON_COLOR,
                fg=TEXT_COLOR
            )
            author_label.pack(anchor="w", pady=3)

            rating_label = tk.Label(
                card,
                text=f"Rating: {rating}",
                font=("Arial", 11),
                bg=BUTTON_COLOR,
                fg=TEXT_COLOR
            )
            rating_label.pack(anchor="w")

    search_button = tk.Button(
        window,
        text="Search",
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=HEADING_COLOR,
        command=search
    )
    search_button.pack(pady=8)

    search_entry.bind("<Return>", lambda event: search())

    close_button = tk.Button(
        window,
        text="Close",
        font=("Arial", 12),
        bg="#52796F",
        fg="white",
        command=window.destroy
    )
    close_button.pack(pady=10)
