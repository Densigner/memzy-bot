"""Flair-related helpers (placeholder)."""

def choose_flair(user_id: str):
    # placeholder logic - replace with actual flair selection
    return "classic" if int(hash(user_id)) % 2 == 0 else "modern"
