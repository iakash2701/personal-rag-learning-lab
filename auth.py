from __future__ import annotations

import hashlib
import json
import os
import secrets
from pathlib import Path
import streamlit as st

USERS_FILE = Path("users.json")


def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    """Hash password using PBKDF2-HMAC-SHA256 with salt."""
    if salt is None:
        salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000,
    )
    return key.hex(), salt.hex()


def load_users() -> dict[str, dict[str, str]]:
    """Load users database from file or initialize with default admin."""
    if not USERS_FILE.exists():
        # Create default admin user
        hash_hex, salt_hex = _hash_password("admin123")
        default_users = {
            "admin": {
                "hash": hash_hex,
                "salt": salt_hex,
            }
        }
        save_users(default_users)
        return default_users

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users: dict[str, dict[str, str]]) -> None:
    """Save users dictionary to JSON file."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def register_user(username: str, password: str) -> tuple[bool, str]:
    """Register a new user account."""
    username = username.strip().lower()
    if not username:
        return False, "Username cannot be empty."
    if len(password) < 4:
        return False, "Password must be at least 4 characters long."

    users = load_users()
    if username in users:
        return False, "Username already exists."

    hash_hex, salt_hex = _hash_password(password)
    users[username] = {
        "hash": hash_hex,
        "salt": salt_hex,
    }
    save_users(users)
    return True, f"Account '{username}' created successfully! You can now log in."


def verify_user(username: str, password: str) -> bool:
    """Verify username and password."""
    username = username.strip().lower()
    users = load_users()
    user = users.get(username)
    if not user:
        return False

    stored_hash = user.get("hash")
    stored_salt = bytes.fromhex(user.get("salt", ""))
    test_hash, _ = _hash_password(password, stored_salt)
    return secrets.compare_digest(stored_hash, test_hash)


def init_auth_state() -> None:
    """Initialize authentication keys in Streamlit session state."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None


def login(username: str, password: str) -> tuple[bool, str]:
    """Attempt to log user in."""
    if verify_user(username, password):
        st.session_state["authenticated"] = True
        st.session_state["user"] = username.strip().lower()
        return True, f"Welcome back, {username}!"
    return False, "Invalid username or password."


def logout() -> None:
    """Log out current user."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
