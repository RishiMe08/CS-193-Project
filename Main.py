
import tkinter as tk

from login import open_login
from user_data import user_has_completed_survey
from survey import open_survey

from library import open_library
from add_book import open_add_book
from rate_book import open_rate_book
from search_book import open_search_books
from recommendations import open_recommendations


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
SECONDARY_COLOR = "#52796F"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


def create_button(parent, text, command):
    button = tk.Button(
        parent,
        text=text,
        font=("Arial", 13),
        bg=BUTTON_COLOR,
        fg=HEADING_COLOR,
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        width=25,
        height=2,
        command=command
    )
    button.pack(pady=8)


def show_home():
    home_frame = tk.Frame(root, bg=BG_COLOR)
    home_frame.pack(fill="both", expand=True)

    heading = tk.Label(
        home_frame,
        text="BookMatch",
        font=("Arial", 28, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    )
    heading.pack(pady=(25, 5))

    subtitle = tk.Label(
        home_frame,
        text="Find your next favorite book",
        font=("Arial", 14),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    subtitle.pack(pady=(0, 20))

    create_button(
        home_frame,
        "View Library",
        lambda: open_library(root)
    )

    create_button(
        home_frame,
        "Add Book",
        lambda: open_add_book(root)
    )

    create_button(
        home_frame,
        "Rate Book",
        lambda: open_rate_book(root)
    )

    create_button(
        home_frame,
        "Search Books",
        lambda: open_search_books(root)
    )

    create_button(
        home_frame,
        "Get Recommendations",
        lambda: open_recommendations(root)
    )

    footer = tk.Label(
        home_frame,
        text="Your personal reading companion",
        font=("Arial", 10),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    footer.pack(pady=20)


def after_login():
    if user_has_completed_survey():
        show_home()
    else:
        open_survey(
            root,
            on_complete=show_home,
            required=True
        )


root = tk.Tk()
root.title("BookMatch")
root.geometry("600x650")
root.configure(bg=BG_COLOR)

open_login(root, after_login)

root.mainloop()
