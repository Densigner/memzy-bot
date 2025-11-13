"""Challenge handling (placeholder)."""
from .storage import Storage

class ChallengeManager:
    def __init__(self, storage: Storage = None):
        self.storage = storage or Storage()

    def add_challenge(self, challenge_id: str, payload: dict):
        challenges = self.storage.get('challenges', {})
        challenges[challenge_id] = payload
        self.storage.set('challenges', challenges)

    def list_challenges(self):
        return list(self.storage.get('challenges', {}).values())
