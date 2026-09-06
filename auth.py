from __future__ import annotations

import hashlib
import re
import secrets
import sqlite3
from pathlib import Path
import streamlit as st

DB_PATH = Path("users.db")


def get_db_connection() -> sqlite3.Connection:
    """Get SQLite database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize SQLite users table and default admin account if empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Create default admin user
            hash_hex, salt_hex = _hash_password("admin123")
            cursor.execute(
                """
                INSERT INTO users (email, username, password_hash, salt)
                VALUES (?, ?, ?, ?)
                """,
                ("admin@example.com", "Admin", hash_hex, salt_hex),
            )
            conn.commit()


def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    """Hash password using PBKDF2-HMAC-SHA256 with 16-byte salt."""
    if salt is None:
        salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000,
    )
    return key.hex(), salt.hex()


def is_valid_email(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))


def register_user(email: str, username: str, password: str) -> tuple[bool, str]:
    """Register a new user in SQLite database."""
    email = email.strip().lower()
    username = username.strip()

    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    if not username:
        return False, "Username cannot be empty."
    if len(password) < 4:
        return False, "Password must be at least 4 characters long."

    hash_hex, salt_hex = _hash_password(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (email, username, password_hash, salt)
                VALUES (?, ?, ?, ?)
                """,
                (email, username, hash_hex, salt_hex),
            )
            conn.commit()
        return True, f"Account created successfully for {email}! You can now log in."
    except sqlite3.IntegrityError:
        return False, f"An account with email '{email}' already exists."
    except Exception as e:
        return False, f"Error creating account: {str(e)}"


def verify_login(email_or_username: str, password: str) -> dict | None:
    """Verify user credentials against SQLite database."""
    query = email_or_username.strip().lower()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(email) = ? OR LOWER(username) = ?",
            (query, query),
        )
        user = cursor.fetchone()

        if not user:
            return None

        stored_hash = user["password_hash"]
        stored_salt = bytes.fromhex(user["salt"])
        test_hash, _ = _hash_password(password, stored_salt)

        if secrets.compare_digest(stored_hash, test_hash):
            return {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
            }
        return None


def init_auth_state() -> None:
    """Initialize SQLite DB and Streamlit session state."""
    init_db()
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = None


def login(email_or_username: str, password: str) -> tuple[bool, str]:
    """Attempt login and store user object in session state."""
    user = verify_login(email_or_username, password)
    if user:
        st.session_state["authenticated"] = True
        st.session_state["user_info"] = user
        return True, f"Welcome back, {user['username']}!"
    return False, "Invalid email/username or password."


def logout() -> None:
    """Log out current user."""
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
