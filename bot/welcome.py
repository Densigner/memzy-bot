"""Welcome message handling (placeholder)."""
from .storage import Storage

class Welcome:
    def __init__(self, storage: Storage = None):
        self.storage = storage or Storage()

    def greet(self, user_name: str) -> str:
        # simple greeting placeholder
        return f"Welcome, {user_name}! Thanks for joining {__import__('os').getenv('BOT_NAME', 'memzy-bot')}"
