
import tkinter as tk
from tkinter import messagebox
import json
import os
import re
import ssl
import certifi

from urllib.request import Request, urlopen
from urllib.parse import urlencode
from html import unescape
from html.parser import HTMLParser
from dotenv import load_dotenv

from user_data import get_preferences_file
from book_data import load_books
from genres import GENRES


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"

load_dotenv()
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


class SummaryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def clean_summary(summary):
    if not summary:
        return "No summary available."

    parser = SummaryParser()
    parser.feed(summary)

    text = " ".join(parser.parts)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_preferences():
    file_path = get_preferences_file()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_list(value):
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def get_preferences_values(preferences, keys):
    values = []

    for key in keys:
        values.extend(get_list(preferences.get(key, [])))

    return values


def get_book_genres(book):
    genre = book.get("genre", book.get("genres", []))

    if isinstance(genre, str):
        genre = [genre]

    return [
        str(item).strip()
        for item in genre
        if str(item).strip()
    ]


def get_rating(book):
    rating = book.get(
        "rating",
        book.get("user_rating", book.get("my_rating", 0))
    )

    try:
        return float(rating)
    except (TypeError, ValueError):
        return 0


def get_liked_books(user_books):
    liked_books = []

    for book in user_books:
        if get_rating(book) >= 4:
            liked_books.append(book)

    return liked_books


def make_search_queries(preferences, user_books):
    queries = []

    preferred_genres = get_preferences_values(
        preferences,
        ["genres", "genre", "favorite_genres", "book_genres"]
    )

    preferred_topics = get_preferences_values(
        preferences,
        ["topics", "favorite_topics", "interests"]
    )

    preferred_authors = get_preferences_values(
        preferences,
        ["favorite_authors", "authors"]
    )

    favorite_titles = get_preferences_values(
        preferences,
        ["favorite_books", "books"]
    )

    liked_books = get_liked_books(user_books)

    # Search for genres selected in the survey.
    for genre in preferred_genres:
        queries.append("subject:" + genre)

    # Search for topics selected in the survey.
    for topic in preferred_topics:
        queries.append(topic)

    # Search for authors selected in the survey.
    for author in preferred_authors:
        queries.append("inauthor:" + author)

    # Search for books similar to favorite titles.
    for title in favorite_titles:
        queries.append(title)

    # Search for more books by authors in the user's library.
    for book in user_books:
        author = book.get("author", "").strip()

        if author:
            queries.append("inauthor:" + author)

    # Search more for authors and genres from highly rated books.
    for book in liked_books:
        author = book.get("author", "").strip()

        if author:
            queries.append("inauthor:" + author)

        for genre in get_book_genres(book):
            queries.append("subject:" + genre)

    # Remove duplicate searches.
    unique_queries = []
    seen = set()

    for query in queries:
        query = query.strip()

        if query and query.lower() not in seen:
            seen.add(query.lower())
            unique_queries.append(query)

    return unique_queries[:10]


def search_google_books(query):
    if not API_KEY:
        raise ValueError(
            "Google Books API key was not found.\n"
            "Check your .env file."
        )

    parameters = {
        "q": query,
        "maxResults": 20,
        "printType": "books",
        "langRestrict": "en",
        "key": API_KEY
    }

    url = (
        "https://www.googleapis.com/books/v1/volumes?"
        + urlencode(parameters)
    )

    request = Request(
        url,
        headers={"User-Agent": "BookMatch/1.0"}
    )

    ssl_context = ssl.create_default_context(
        cafile=certifi.where()
    )

    with urlopen(
        request,
        timeout=20,
        context=ssl_context
    ) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    books = []

    for item in data.get("items", []):
        info = item.get("volumeInfo", {})

        title = info.get("title", "").strip()

        if not title:
            continue

        authors = info.get("authors", ["Unknown author"])
        categories = info.get("categories", [])

        books.append({
            "id": item.get("id", ""),
            "title": title,
            "author": ", ".join(authors),
            "summary": clean_summary(
                info.get("description", "")
            ),
            "genre": categories,
            "year": info.get("publishedDate", "Unknown"),
            "rating": info.get("averageRating", 0)
        })

    return books


def get_recommendations():
    preferences = load_preferences()
    user_books = load_books()

    queries = make_search_queries(
        preferences,
        user_books
    )

    if not queries:
        return []

    # Exclude books already in the user's library.
    read_titles = {
        book.get("title", "").strip().lower()
        for book in user_books
    }

    found_books = {}

    for query in queries:
        try:
            results = search_google_books(query)
        except Exception as error:
            print(f"Google Books search failed: {error}")
            continue

        for book in results:
            title = book.get("title", "").strip().lower()

            if title in read_titles:
                continue

            book_id = book.get("id", "")

            if not book_id:
                book_id = title + book.get("author", "").lower()

            found_books[book_id] = book

    preferred_genres = get_preferences_values(
        preferences,
        ["genres", "genre", "favorite_genres", "book_genres"]
    )

    preferred_topics = get_preferences_values(
        preferences,
        ["topics", "favorite_topics", "interests"]
    )

    preferred_authors = get_preferences_values(
        preferences,
        ["favorite_authors", "authors"]
    )

    liked_books = get_liked_books(user_books)

    liked_authors = [
        book.get("author", "").strip().lower()
        for book in liked_books
        if book.get("author", "").strip()
    ]

    library_authors = [
        book.get("author", "").strip().lower()
        for book in user_books
        if book.get("author", "").strip()
    ]

    liked_genres = []

    for book in liked_books:
        liked_genres.extend(get_book_genres(book))

    scored_books = []

    for book in found_books.values():
        title = book.get("title", "").lower()
        author = book.get("author", "").lower()
        summary = book.get("summary", "").lower()

        genres = [
            genre.lower()
            for genre in get_book_genres(book)
        ]

        score = 0

        # Match genres from the survey.
        for genre in preferred_genres:
            if any(genre.lower() in item for item in genres):
                score += 5

        # Match genres from highly rated books.
        for genre in liked_genres:
            if any(genre.lower() in item for item in genres):
                score += 4

        # Match topics from the survey.
        for topic in preferred_topics:
            if topic.lower() in title or topic.lower() in summary:
                score += 3

        # Match authors the user selected in the survey.
        for preferred_author in preferred_authors:
            if preferred_author.lower() in author:
                score += 5

        # Strongly recommend more books by highly rated authors.
        for liked_author in liked_authors:
            if liked_author in author:
                score += 8

        # Also recommend authors from the user's library.
        for library_author in library_authors:
            if library_author in author:
                score += 3

        # Use Google Books' average rating as a small bonus.
        try:
            score += float(book.get("rating", 0))
        except (TypeError, ValueError):
            pass

        scored_books.append((score, book))

    scored_books.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        book
        for score, book in scored_books[:20]
    ]


def open_recommendations(parent):
    window = tk.Toplevel(parent)
    window.title("BookMatch - Recommendations")
    window.geometry("750x600")
    window.configure(bg=BG_COLOR)

    heading = tk.Label(
        window,
        text="Recommended Books",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    )
    heading.pack(pady=15)

    description = tk.Label(
        window,
        text="Recommendations based on your survey and reading history",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        wraplength=650
    )
    description.pack(pady=5)

    list_frame = tk.Frame(window, bg=BG_COLOR)
    list_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    canvas = tk.Canvas(
        list_frame,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        list_frame,
        orient="vertical",
        command=canvas.yview
    )

    book_frame = tk.Frame(canvas, bg=BG_COLOR)

    book_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=book_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def display_books():
        for widget in book_frame.winfo_children():
            widget.destroy()

        try:
            recommendations = get_recommendations()
        except Exception as error:
            messagebox.showerror(
                "Recommendations",
                str(error)
            )
            return

        if not recommendations:
            message = tk.Label(
                book_frame,
                text="No recommendations found.\n"
                     "Try adding books, rating them, or updating your survey.",
                font=("Arial", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                wraplength=600
            )
            message.pack(pady=30)
            return

        for book in recommendations:
            card = tk.Frame(
                book_frame,
                bg=BUTTON_COLOR,
                padx=12,
                pady=10
            )
            card.pack(fill="x", pady=7)

            title = book.get("title", "Unknown title")
            author = book.get("author", "Unknown author")
            summary = book.get("summary", "No summary available.")
            year = book.get("year", "Unknown")

            title_label = tk.Label(
                card,
                text=title,
                font=("Arial", 15, "bold"),
                bg=BUTTON_COLOR,
                fg=HEADING_COLOR,
                wraplength=620,
                justify="left"
            )
            title_label.pack(anchor="w")

            author_label = tk.Label(
                card,
                text=f"By {author} | {year}",
                font=("Arial", 11),
                bg=BUTTON_COLOR,
                fg=TEXT_COLOR,
                wraplength=620,
                justify="left"
            )
            author_label.pack(anchor="w", pady=3)

            summary_label = tk.Label(
                card,
                text=summary,
                font=("Arial", 10),
                bg=BUTTON_COLOR,
                fg=TEXT_COLOR,
                wraplength=620,
                justify="left"
            )
            summary_label.pack(anchor="w", pady=3)

    refresh_button = tk.Button(
        window,
        text="Refresh Recommendations",
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=HEADING_COLOR,
        command=display_books
    )
    refresh_button.pack(pady=8)

    close_button = tk.Button(
        window,
        text="Close",
        font=("Arial", 12),
        bg="#52796F",
        fg="white",
        command=window.destroy
    )
    close_button.pack(pady=10)

    display_books()
