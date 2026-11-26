
import tkinter as tk
from tkinter import ttk

# Create the application window
window = tk.Tk()
window.title("BookMatch")
window.geometry("900x600")
window.configure(bg="#F5F0E8")

# Create the title
title_label = tk.Label(
    window,
    text="BookMatch",
    font=("Georgia", 28, "bold"),
    bg="#F5F0E8",
    fg="#4A3528"
)
title_label.pack(pady=(20, 5))

welcome_label = tk.Label(
    window,
    text="Find your next favorite book",
    font=("Arial", 12),
    bg="#F5F0E8",
    fg="#6B5B4D"
)
welcome_label.pack(pady=(0, 15))

# Create the search section
search_frame = tk.Frame(window, bg="#F5F0E8")
search_frame.pack(pady=10)

search_label = tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 12),
    bg="#F5F0E8"
)
search_label.pack(side="left", padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 12)
)
search_entry.pack(side="left", padx=5)

search_button = tk.Button(
    search_frame,
    text="Search",
    font=("Arial", 11),
    bg="#D8C3A5"
)
search_button.pack(side="left", padx=5)

# Create the main content area
content_frame = tk.Frame(window, bg="#F5F0E8")
content_frame.pack(fill="both", expand=True, padx=25, pady=15)

# Create the book library section
library_frame = tk.LabelFrame(
    content_frame,
    text="My Library",
    font=("Arial", 14, "bold"),
    bg="#F5F0E8",
    fg="#4A3528",
    padx=10,
    pady=10
)
library_frame.pack(side="left", fill="both", expand=True, padx=10)

# Create category buttons
category_frame = tk.Frame(library_frame, bg="#F5F0E8")
category_frame.pack(fill="x", pady=5)

read_button = tk.Button(
    category_frame,
    text="Read",
    bg="#D8C3A5"
)
read_button.pack(side="left", padx=5)

reading_button = tk.Button(
    category_frame,
    text="Currently Reading",
    bg="#D8C3A5"
)
reading_button.pack(side="left", padx=5)

want_button = tk.Button(
    category_frame,
    text="Want to Read",
    bg="#D8C3A5"
)
want_button.pack(side="left", padx=5)

# Create a sample book list
book_list = tk.Listbox(
    library_frame,
    font=("Arial", 12),
    height=15,
    width=35
)
book_list.pack(fill="both", expand=True, pady=10)

book_list.insert("end", "The Hunger Games - Suzanne Collins")
book_list.insert("end", "The Hobbit - J.R.R. Tolkien")
book_list.insert("end", "Pride and Prejudice - Jane Austen")

# Create the book details section
details_frame = tk.LabelFrame(
    content_frame,
    text="Book Details",
    font=("Arial", 14, "bold"),
    bg="#F5F0E8",
    fg="#4A3528",
    padx=15,
    pady=15
)
details_frame.pack(side="right", fill="both", expand=True, padx=10)

details_label = tk.Label(
    details_frame,
    text="Select a book to see its details.",
    font=("Arial", 12),
    bg="#F5F0E8",
    wraplength=250
)
details_label.pack(pady=20)

# Create the add book button
add_button = tk.Button(
    details_frame,
    text="Add Book",
    font=("Arial", 12),
    bg="#A3B18A",
    width=15
)
add_button.pack(pady=10)

# Create the rating button
rating_button = tk.Button(
    details_frame,
    text="Rate Book",
    font=("Arial", 12),
    bg="#D8C3A5",
    width=15
)
rating_button.pack(pady=10)

# Keep the application window open
window.mainloop()
