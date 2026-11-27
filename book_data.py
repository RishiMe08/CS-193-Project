
import json
from pathlib import Path


FILE_PATH = Path(__file__).parent / "books.json"


def load_books():
    if not FILE_PATH.exists():
        save_books([])
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_books(books):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)


def add_book(book):
    books = load_books()
    books.append(book)
    save_books(books)


def update_book(index, updated_book):
    books = load_books()

    if 0 <= index < len(books):
        books[index] = updated_book
        save_books(books)


def get_books():
    return load_books()
