"""Leaderboard utilities (placeholder)."""
from .counters import Counters

class Leaderboard:
    def __init__(self, counters: Counters = None):
        self.counters = counters or Counters()

    def top_n(self, n: int = 10):
        return self.counters.top(n)
