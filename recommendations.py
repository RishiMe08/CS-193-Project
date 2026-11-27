
import tkinter as tk
import json
import re
from book_database import load_catalog


def load_preferences():
    try:
        with open("preferences.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_books():
    try:
        with open("books.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_recommendations():
    preferences = load_preferences()
    catalog = load_catalog()
    library = load_books()

    if not catalog:
        return [], "Your book catalog is empty. Run book_database.py first."

    if not preferences:
        return [], "Please take the BookMatch survey first."

    preferred_answers = []

    for answers in preferences.values():
        if isinstance(answers, list):
            preferred_answers.extend(answers)

        elif isinstance(answers, str):
            preferred_answers.append(answers)

    if not preferred_answers:
        return [], "Please select some answers in the survey."

    owned_titles = {
        book.get("title", "").strip().lower()
        for book in library
    }

    recommendations = []

    for book in catalog:
        title = book.get("title", "").strip()

        if not title:
            continue

        if title.lower() in owned_titles:
            continue

        genres = book.get("genre", [])

        if isinstance(genres, str):
            genres = [genres]

        genre_text = " ".join(genres).lower()
        summary = book.get("summary", "").lower()
        author = book.get("author", "").lower()
        title_text = title.lower()

        score = 0

        for answer in preferred_answers:
            answer = str(answer).strip().lower()

            if not answer:
                continue

            if answer in genre_text:
                score += 3

            elif answer in title_text:
                score += 2

            elif answer in summary:
                score += 1

        if score > 0:
            book_copy = book.copy()
            book_copy["score"] = score
            recommendations.append(book_copy)

    recommendations.sort(
        key=lambda book: book["score"],
        reverse=True
    )

    return recommendations[:20], None


def open_recommendations(parent):
    window = tk.Toplevel(parent)
    window.title("BookMatch Recommendations")
    window.geometry("700x600")
    window.configure(bg="#CAD2C5")

    heading = tk.Label(
        window,
        text="BookMatch Recommendations",
        font=("Arial", 20, "bold"),
        bg="#CAD2C5",
        fg="#354F52"
    )
    heading.pack(pady=15)

    description = tk.Label(
        window,
        text="Books selected based on your survey answers",
        font=("Arial", 11),
        bg="#CAD2C5",
        fg="#2F3E46"
    )
    description.pack(pady=5)

    results_frame = tk.Frame(window, bg="#CAD2C5")
    results_frame.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side="right", fill="y")

    results_list = tk.Listbox(
        results_frame,
        font=("Arial", 11),
        bg="#FFFFFF",
        fg="#2F3E46",
        yscrollcommand=scrollbar.set,
        selectmode=tk.SINGLE,
        width=70,
        height=15
    )
    results_list.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=results_list.yview)

    details_label = tk.Label(
        window,
        text="Select a book to see its summary.",
        font=("Arial", 10),
        bg="#CAD2C5",
        fg="#2F3E46",
        wraplength=640,
        justify="left"
    )
    details_label.pack(padx=20, pady=10)

    books, error_message = get_recommendations()

    if error_message:
        results_list.insert(tk.END, error_message)

    elif not books:
        results_list.insert(
            tk.END,
            "No matching books found. Try different survey answers."
        )

    else:
        for book in books:
            results_list.insert(
                tk.END,
                book.get("title", "Unknown title")
            )

    def show_details(event):
        selection = results_list.curselection()

        if not selection or not books:
            return

        index = selection[0]

        if index >= len(books):
            return

        book = books[index]

        title = book.get("title", "Unknown title")
        author = book.get("author", "Unknown author")
        summary = book.get("summary", "No summary available.")
        genres = book.get("genre", [])
        year = book.get("year", "Unknown")

        if isinstance(genres, list):
            genres = ", ".join(genres)

        details = (
            f"Title: {title}\n"
            f"Author: {author}\n"
            f"Genre: {genres}\n"
            f"Year: {year}\n\n"
            f"Summary: {summary}"
        )

        details_label.config(text=details)

    results_list.bind("<<ListboxSelect>>", show_details)

    close_button = tk.Button(
        window,
        text="Close",
        font=("Arial", 11),
        bg="#84A98C",
        fg="#2F3E46",
        command=window.destroy
    )
    close_button.pack(pady=10)
 