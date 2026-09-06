from __future__ import annotations


def format_similarity_percentage(similarity: float) -> str:
    """Format similarity score as percentage string."""
    percentage = max(0, min(100, int(similarity * 100)))
    return f"{percentage}%"


def get_similarity_color(similarity: float) -> str:
    """Return color hex based on similarity threshold."""
    if similarity >= 0.71:
        return "#22C55E"  # High relevance (Green)
    elif similarity >= 0.41:
        return "#6366F1"  # Moderate relevance (Indigo)
    else:
        return "#71717A"  # Low relevance (Muted)


def format_vector_slice(vector: list[float] | tuple[float, ...], limit: int = 20) -> str:
    """Format float vector values for clean code view."""
    return str([round(float(v), 6) for v in vector[:limit]])
