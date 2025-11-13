import json, os

STATE_DIR = "state"
COUNTS_PATH = os.path.join(STATE_DIR, "counts.json")
META_PATH   = os.path.join(STATE_DIR, "meta.json")

EMPTY = { "users": {} }

META_EMPTY = {
    "last_seen_submission": "",
    "last_seen_comment": "",
    "welcomed_posts": [],
    "weekly_threads": {
        "leaderboard_post_id": "",
        "challenge_post_id": ""
    }
}

def _ensure():
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(COUNTS_PATH):
        with open(COUNTS_PATH, "w", encoding="utf-8") as f: json.dump(EMPTY, f, indent=2)
    if not os.path.exists(META_PATH):
        with open(META_PATH, "w", encoding="utf-8") as f: json.dump(META_EMPTY, f, indent=2)

def load_counts():
    _ensure()
    with open(COUNTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_counts(data):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(COUNTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_meta():
    _ensure()
    with open(META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_meta(meta):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
