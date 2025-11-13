"""Configuration for memzy-bot."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

# file used to persist simple state
STATE_FILE = STATE_DIR / "state.json"

# default values
BOT_NAME = "memzy-bot"
