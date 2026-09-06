from __future__ import annotations

import re
from datetime import datetime


def sanitize_filename(name: str) -> str:
    """Sanitize string for clean identifier representation."""
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name.lower())


def get_user_initials(name: str) -> str:
    """Extract initials from username or full name."""
    if not name:
        return "U"
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[:2].upper()


def get_current_timestamp() -> str:
    """Format current timestamp for display."""
    return datetime.now().strftime("%b %d, %Y • %H:%M")
