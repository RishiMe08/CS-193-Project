import tkinter as tk

from book_data import load_books


BG_COLOR = "#CAD2C5"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_recommendations(parent):
    window = tk.Toplevel(parent)
    window.title("Recommendations")
    window.geometry("500x500")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="Your Recommendations",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    results = tk.Listbox(
        window,
        width=45,
        height=18,
        font=("Arial", 12),
        bg="white",
        fg=TEXT_COLOR
    )
    results.pack(pady=10)

    books = load_books()

    recommended_books = [
        book for book in books
        if book["rating"] >= 4
    ]

    if not recommended_books:
        results.insert(
            tk.END,
            "Rate books to get recommendations."
        )

    for book in recommended_books:
        results.insert(
            tk.END,
            f"{book['title']} - Rating: {book['rating']}/5"
        )

    return window