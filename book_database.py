
import os
import json
import re
import time
import ssl
import certifi
from html import unescape
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
CATALOG_FILE = "book_catalog.json"

GENRES = [
    "Fantasy",
    "Science Fiction",
    "Mystery",
    "Romance",
    "Thriller",
    "Horror",
    "Historical Fiction",
    "Young Adult",
    "Adventure",
    "Biography",
    "Psychology",
    "Classics"
]


class DescriptionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


def clean_description(description):
    if not description:
        return "No summary available."

    parser = DescriptionParser()
    parser.feed(description)

    text = " ".join(parser.text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def search_books_by_subject(subject, pages=2):
    books = []

    if not API_KEY:
        print("Google Books API key was not found.")
        print("Check your .env file.")
        return books

    ssl_context = ssl.create_default_context(
        cafile=certifi.where()
    )

    for page in range(pages):
        parameters = {
            "q": f"subject:{subject}",
            "maxResults": 40,
            "startIndex": page * 40,
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

        try:
            with urlopen(
                request,
                timeout=20,
                context=ssl_context
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

        except Exception as error:
            print(f"Could not search {subject}: {error}")
            break

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
                "summary": clean_description(
                    info.get("description", "")
                ),
                "genre": categories,
                "year": info.get("publishedDate", "Unknown"),
                "rating": info.get("averageRating", 0)
            })

        time.sleep(0.5)

    return books


def build_catalog():
    catalog = {}

    for genre in GENRES:
        print(f"Searching for {genre} books...")

        books = search_books_by_subject(genre, pages=2)

        for book in books:
            book_id = book.get("id", "")

            if not book_id:
                book_id = (
                    book["title"].lower()
                    + book["author"].lower()
                )

            if book_id not in catalog:
                catalog[book_id] = book

    saved_books = list(catalog.values())

    with open(CATALOG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            saved_books,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nBook catalog created!")
    print(f"Total unique books: {len(saved_books)}")
    print(f"Saved in: {CATALOG_FILE}")


def load_catalog():
    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


if __name__ == "__main__":
    build_catalog()
