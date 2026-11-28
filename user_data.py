
import json
import hashlib
import os
from pathlib import Path


BASE_FOLDER = Path(__file__).parent
USERS_FILE = BASE_FOLDER / "users.json"
DATA_FOLDER = BASE_FOLDER / "user_data"

current_user = None


def set_current_user(username):
    global current_user
    current_user = username


def get_current_user():
    return current_user


def get_user_folder():
    if not current_user:
        raise ValueError("No user is logged in.")

    folder = DATA_FOLDER / current_user
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_books_file():
    return get_user_folder() / "books.json"


def get_preferences_file():
    return get_user_folder() / "preferences.json"


def load_users():
    if not USERS_FILE.exists():
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def hash_password(password, salt):
    password_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")

    return hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt_bytes,
        200000
    ).hex()


def create_account(username, password):
    username = username.strip().lower()

    if not username or not password:
        return False, "Enter a username and password."

    users = load_users()

    if username in users:
        return False, "That username already exists."

    salt = os.urandom(16).hex()
    password_hash = hash_password(password, salt)

    users[username] = {
        "salt": salt,
        "password_hash": password_hash
    }

    save_users(users)

    return True, "Account created."


def login_user(username, password):
    username = username.strip().lower()
    users = load_users()

    if username not in users:
        return False, "Username or password is incorrect."

    user = users[username]
    password_hash = hash_password(password, user["salt"])

    if password_hash != user["password_hash"]:
        return False, "Username or password is incorrect."

    set_current_user(username)

    return True, "Login successful."


def user_has_completed_survey():
    preferences_file = get_preferences_file()

    if not preferences_file.exists():
        return False

    try:
        with open(preferences_file, "r", encoding="utf-8") as file:
            preferences = json.load(file)

        return bool(preferences)

    except (json.JSONDecodeError, OSError):
        return False
