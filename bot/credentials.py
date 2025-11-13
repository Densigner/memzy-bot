"""Load Reddit bot credentials from environment variables or .env file.

Usage:
  - Create a `.env` file from `.env.example` and fill values.
  - `pip install python-dotenv` to load .env automatically, or set env vars in your OS.
"""
import os
from pathlib import Path
from typing import Optional

# Optionally load .env (soft dependency)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not installed; assume environment variables are set by other means
    pass


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)

REDDIT_CLIENT_ID = get_env('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = get_env('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = get_env('REDDIT_USERNAME')
REDDIT_PASSWORD = get_env('REDDIT_PASSWORD')
SUBREDDIT = get_env('SUBREDDIT', 'memzy')
BOT_USERNAME = get_env('BOT_USERNAME', REDDIT_USERNAME)

# Basic validation helper
def validate_credentials() -> bool:
    missing = [k for k in ('REDDIT_CLIENT_ID','REDDIT_CLIENT_SECRET','REDDIT_USERNAME','REDDIT_PASSWORD') if not get_env(k)]
    if missing:
        return False
    return True

if __name__ == '__main__':
    print('Credentials loaded:')
    print('REDDIT_CLIENT_ID:', 'set' if REDDIT_CLIENT_ID else 'missing')
    print('REDDIT_CLIENT_SECRET:', 'set' if REDDIT_CLIENT_SECRET else 'missing')
    print('REDDIT_USERNAME:', REDDIT_USERNAME)
    print('SUBREDDIT:', SUBREDDIT)
    print('BOT_USERNAME:', BOT_USERNAME)
