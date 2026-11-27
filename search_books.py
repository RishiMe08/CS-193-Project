import tkinter as tk

from book_data import load_books


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_search_books(parent):
    window = tk.Toplevel(parent)
    window.title("Search Books")
    window.geometry("500x500")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="Search Your Library",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    search_entry = tk.Entry(window, width=35, font=("Arial", 12))
    search_entry.pack(pady=10)

    results = tk.Listbox(
        window,
        width=45,
        height=18,
        font=("Arial", 12),
        bg="white",
        fg=TEXT_COLOR
    )
    results.pack(pady=10)

    def search():
        results.delete(0, tk.END)

        search_text = search_entry.get().lower()
        books = load_books()

        for book in books:
            title = book["title"].lower()
            author = book["author"].lower()
            genre = book["genre"].lower()

            if (
                search_text in title
                or search_text in author
                or search_text in genre
            ):
                results.insert(
                    tk.END,
                    f"{book['title']} by {book['author']}"
                )

    tk.Button(
        window,
        text="Search",
        command=search,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=20
    ).pack(pady=5)

    return window