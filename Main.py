import tkinter as tk
from tkinter import ttk

# BookMatch color palette
backgroundColor = "#CAD2C5"
buttonColor = "#84A98C"
secondaryColor = "#52796F"
headingColor = "#354F52"
textColor = "#2F3E46"

# Create the main window
window = tk.Tk()
window.title("BookMatch")
window.geometry("900x600")
window.configure(bg=backgroundColor)

# Main title
titleLabel = tk.Label(
    window,
    text="BookMatch",
    font=("Arial", 28, "bold"),
    bg=backgroundColor,
    fg=headingColor
)
titleLabel.pack(pady=15)

# Welcome message
welcomeLabel = tk.Label(
    window,
    text="Find your next favorite book!",
    font=("Arial", 14),
    bg=backgroundColor,
    fg=textColor
)
welcomeLabel.pack(pady=5)

# Search section
searchFrame = tk.Frame(window, bg=backgroundColor)
searchFrame.pack(pady=15)

searchEntry = tk.Entry(
    searchFrame,
    width=40,
    font=("Arial", 12),
    bg="white",
    fg=textColor
)
searchEntry.pack(side=tk.LEFT, padx=5)

searchButton = tk.Button(
    searchFrame,
    text="Search",
    font=("Arial", 11),
    bg=buttonColor,
    fg=textColor,
    activebackground=secondaryColor,
    activeforeground="white"
)
searchButton.pack(side=tk.LEFT, padx=5)

# Main content area
contentFrame = tk.Frame(window, bg=backgroundColor)
contentFrame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Library section
libraryFrame = tk.LabelFrame(
    contentFrame,
    text="My Library",
    font=("Arial", 14, "bold"),
    bg=backgroundColor,
    fg=headingColor,
    padx=10,
    pady=10
)
libraryFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# Reading category buttons
readButton = tk.Button(
    libraryFrame,
    text="Read",
    width=15,
    bg=buttonColor,
    fg=textColor,
    activebackground=secondaryColor,
    activeforeground="white"
)
readButton.pack(pady=5)

currentlyReadingButton = tk.Button(
    libraryFrame,
    text="Currently Reading",
    width=15,
    bg=secondaryColor,
    fg="white",
    activebackground=headingColor,
    activeforeground="white"
)
currentlyReadingButton.pack(pady=5)

wantToReadButton = tk.Button(
    libraryFrame,
    text="Want to Read",
    width=15,
    bg=headingColor,
    fg="white",
    activebackground=textColor,
    activeforeground="white"
)
wantToReadButton.pack(pady=5)

# Sample book list
bookList = tk.Listbox(
    libraryFrame,
    font=("Arial", 12),
    bg="white",
    fg=textColor,
    selectbackground=secondaryColor,
    selectforeground="white"
)
bookList.pack(fill=tk.BOTH, expand=True, pady=10)

bookList.insert(tk.END, "The Hunger Games")
bookList.insert(tk.END, "The Book Thief")
bookList.insert(tk.END, "Pride and Prejudice")

# Book details section
detailsFrame = tk.LabelFrame(
    contentFrame,
    text="Book Details",
    font=("Arial", 14, "bold"),
    bg=backgroundColor,
    fg=headingColor,
    padx=10,
    pady=10
)
detailsFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

detailsLabel = tk.Label(
    detailsFrame,
    text="Select a book to see its details.",
    font=("Arial", 12),
    bg=backgroundColor,
    fg=textColor,
    wraplength=250
)
detailsLabel.pack(pady=20)

# Add book button
addBookButton = tk.Button(
    detailsFrame,
    text="Add Book",
    font=("Arial", 12),
    bg=buttonColor,
    fg=textColor,
    activebackground=secondaryColor,
    activeforeground="white"
)
addBookButton.pack(pady=10)

# Rate book button
rateBookButton = tk.Button(
    detailsFrame,
    text="Rate Book",
    font=("Arial", 12),
    bg=secondaryColor,
    fg="white",
    activebackground=headingColor,
    activeforeground="white"
)
rateBookButton.pack(pady=10)

# Start the application
window.mainloop()