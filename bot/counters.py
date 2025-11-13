"""Counter utilities for memzy-bot."""
from .storage import Storage

class Counters:
    def __init__(self, storage: Storage = None):
        self.storage = storage or Storage()

    def increment(self, name: str, by: int = 1) -> int:
        counts = self.storage.get('counters', {})
        counts[name] = counts.get(name, 0) + by
        self.storage.set('counters', counts)
        return counts[name]

    def get(self, name: str) -> int:
        return self.storage.get('counters', {}).get(name, 0)

    def top(self, n: int = 10):
        counts = self.storage.get('counters', {})
        return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]
