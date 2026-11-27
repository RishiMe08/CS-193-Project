import json
import os


FILE_NAME = "books.json"


def load_books():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            books = json.load(file)

        return books

    except (json.JSONDecodeError, OSError):
        return []


def save_books(books):
    with open(FILE_NAME, "w") as file:
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