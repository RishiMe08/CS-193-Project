
import tkinter as tk

from book_data import load_books


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def open_search_books(parent):
    window = tk.Toplevel(parent)
    window.title("Search Books")
    window.geometry("600x600")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="Search Books",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=20)

    tk.Label(
        window,
        text="Search by title, author, or genre",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    search_entry = tk.Entry(
        window,
        width=40,
        font=("Arial", 12)
    )
    search_entry.pack(pady=10)

    tk.Label(
        window,
        text="Filter by Reading Status",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(10, 5))

    status_filter = tk.StringVar(value="All Books")

    status_menu = tk.OptionMenu(
        window,
        status_filter,
        "All Books",
        "Read",
        "Currently Reading",
        "Want to Read"
    )
    status_menu.configure(
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_COLOR
    )
    status_menu.pack()

    results = tk.Listbox(
        window,
        width=55,
        height=15,
        font=("Arial", 12),
        bg="white",
        fg=TEXT_COLOR
    )
    results.pack(pady=15)

    details = tk.Label(
        window,
        text="Select a book to see its details.",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        wraplength=500
    )
    details.pack(pady=10)

    matching_books = []

    def search_books():
        results.delete(0, tk.END)
        details.config(text="Select a book to see its details.")

        search_text = search_entry.get().strip().lower()
        selected_status = status_filter.get()

        books = load_books()
        matching_books.clear()

        for book in books:
            title = book.get("title", "").lower()
            author = book.get("author", "").lower()
            genre = book.get("genre", "").lower()
            status = book.get("status", "")

            matches_text = (
                search_text in title
                or search_text in author
                or search_text in genre
            )

            matches_status = (
                selected_status == "All Books"
                or status == selected_status
            )

            if matches_text and matches_status:
                matching_books.append(book)

                results.insert(
                    tk.END,
                    f"{book.get('title', 'Unknown')} - "
                    f"{book.get('author', 'Unknown')}"
                )

        if not matching_books:
            results.insert(tk.END, "No matching books found.")

    def show_details(event):
        selection = results.curselection()

        if not selection:
            return

        index = selection[0]

        if index >= len(matching_books):
            return

        book = matching_books[index]

        rating = book.get("rating", 0)

        if rating == 0:
            rating_text = "Not rated"
        else:
            rating_text = f"{rating}/5"

        details.config(
            text=(
                f"Title: {book.get('title', '')}\n"
                f"Author: {book.get('author', '')}\n"
                f"Genre: {book.get('genre', '')}\n"
                f"Status: {book.get('status', '')}\n"
                f"Rating: {rating_text}"
            )
        )

    search_button = tk.Button(
        window,
        text="Search",
        command=search_books,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=20
    )
    search_button.pack(pady=5)

    results.bind("<<ListboxSelect>>", show_details)

    status_filter.trace_add(
        "write",
        lambda *args: search_books()
    )

    search_entry.bind(
        "<Return>",
        lambda event: search_books()
    )

    search_books()

    return window
