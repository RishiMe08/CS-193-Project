
import tkinter as tk

from library import open_library
from add_book import open_add_book
from rate_book import open_rate_book
from search_books import open_search_books
from recommendations import open_recommendations
from find_books import open_find_books


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def create_button(parent, text, command):
    """Create a button for the home window."""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 13),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_COLOR,
        activeforeground=TEXT_COLOR,
        width=25,
        height=2,
        relief="flat",
        cursor="hand2"
    )
    button.pack(pady=7)


root = tk.Tk()
root.title("BookMatch")
root.geometry("600x650")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

title = tk.Label(
    root,
    text="BookMatch",
    font=("Arial", 32, "bold"),
    bg=BG_COLOR,
    fg=HEADING_COLOR
)
title.pack(pady=(35, 5))

subtitle = tk.Label(
    root,
    text="Find your next favorite book",
    font=("Arial", 15),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
subtitle.pack(pady=(0, 25))

create_button(
    root,
    "View Library",
    lambda: open_library(root)
)

create_button(
    root,
    "Add Book",
    lambda: open_add_book(root)
)

create_button(
    root,
    "Rate Book",
    lambda: open_rate_book(root)
)

create_button(
    root,
    "Search Books",
    lambda: open_search_books(root)
)

create_button(
    root,
    "Get Recommendations",
    lambda: open_recommendations(root)
)

create_button(
    root,
    "Find New Books",
    lambda: open_find_books(root)
)

footer = tk.Label(
    root,
    text="Your personal reading companion",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
footer.pack(side="bottom", pady=20)

root.mainloop()
