
import tkinter as tk
from tkinter import messagebox
import json

from user_data import get_preferences_file


BG_COLOR = "#CAD2C5"
BUTTON_COLOR = "#84A98C"
HEADING_COLOR = "#354F52"
TEXT_COLOR = "#2F3E46"


QUESTIONS = [
    {
        "question": "1. What genres do you enjoy?",
        "options": [
            "Fantasy", "Mystery", "Romance", "Science Fiction",
            "Thriller", "Historical Fiction", "Horror",
            "Adventure", "Nonfiction", "Biography"
        ]
    },
    {
        "question": "2. What themes interest you?",
        "options": [
            "Friendship", "Adventure", "Personal Growth", "Family",
            "Science and Technology", "History", "Humor", "Love",
            "Survival", "Problem Solving"
        ]
    },
    {
        "question": "3. What reading style do you prefer?",
        "options": [
            "Fast-paced", "Slow-paced", "Lots of action",
            "Detailed descriptions", "Plot twists",
            "Character-focused", "Thought-provoking"
        ]
    },
    {
        "question": "4. What book length do you prefer?",
        "options": [
            "Short books", "Medium-length books",
            "Long books", "Any length"
        ]
    },
    {
        "question": "5. What kinds of stories interest you?",
        "options": [
            "Realistic stories", "Imaginary worlds", "True stories",
            "Dystopian worlds", "Coming-of-age stories",
            "Detective stories", "Inspirational stories",
            "Survival stories"
        ]
    }
]


def load_preferences():
    file_path = get_preferences_file()

    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_preferences(preferences):
    file_path = get_preferences_file()

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(preferences, file, indent=4)


def open_survey(parent, on_complete=None, required=False):
    window = tk.Toplevel(parent)
    window.title("BookMatch Survey")
    window.geometry("650x750")
    window.configure(bg=BG_COLOR)

    if required:
        window.transient(parent)
        window.grab_set()
        window.protocol("WM_DELETE_WINDOW", lambda: None)

    tk.Label(
        window,
        text="BookMatch Survey",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=HEADING_COLOR
    ).pack(pady=15)

    tk.Label(
        window,
        text="Select all answers that match your interests.",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=5)

    saved_preferences = load_preferences()
    listboxes = {}

    content = tk.Frame(window, bg=BG_COLOR)
    content.pack(fill="both", expand=True, padx=20)

    for question in QUESTIONS:
        question_frame = tk.Frame(content, bg=BG_COLOR)
        question_frame.pack(fill="x", pady=8)

        tk.Label(
            question_frame,
            text=question["question"],
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=HEADING_COLOR
        ).pack(anchor="w")

        listbox = tk.Listbox(
            question_frame,
            selectmode=tk.MULTIPLE,
            height=4,
            exportselection=False,
            font=("Arial", 11),
            bg="white",
            fg=TEXT_COLOR
        )
        listbox.pack(fill="x", pady=4)

        for option in question["options"]:
            listbox.insert(tk.END, option)

        saved_answers = saved_preferences.get(
            question["question"],
            []
        )

        for index, option in enumerate(question["options"]):
            if option in saved_answers:
                listbox.selection_set(index)

        listboxes[question["question"]] = listbox

    def save_survey():
        preferences = {}

        for question, listbox in listboxes.items():
            selected_answers = [
                listbox.get(index)
                for index in listbox.curselection()
            ]

            preferences[question] = selected_answers

        if not any(preferences.values()):
            messagebox.showwarning(
                "Choose Answers",
                "Please select at least one answer.",
                parent=window
            )
            return

        save_preferences(preferences)

        messagebox.showinfo(
            "Survey Saved",
            "Your preferences have been saved!",
            parent=window
        )

        window.destroy()

        if on_complete:
            on_complete()

    tk.Button(
        window,
        text="Save Preferences",
        command=save_survey,
        font=("Arial", 12),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=22
    ).pack(pady=15)

    return window
