
import json

from user_data import get_books_file


def load_books():
    file_path = get_books_file()

    if not file_path.exists():
        save_books([])
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_books(books):
    file_path = get_books_file()

    with open(file_path, "w", encoding="utf-8") as file:
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
