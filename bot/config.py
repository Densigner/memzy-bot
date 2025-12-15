import os

# Try to load a local .env file if available (dev convenience)
try:
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	pass


def env_bool(name, default="false"):
	return os.getenv(name, default).lower() in ("1", "true", "yes", "y", "on")


# Use getenv so missing values don't raise KeyError at import time. Callers should
# validate credentials before attempting network calls.
CONFIG = {
    "client_id": os.getenv("REDDIT_CLIENT_ID", ""),
    "client_secret": os.getenv("REDDIT_CLIENT_SECRET", ""),
    # read the OAuth refresh token from the environment
    "refresh_token": os.getenv("REDDIT_REFRESH_TOKEN", ""),
    "username": os.getenv("REDDIT_USERNAME", ""),
    "password": os.getenv("REDDIT_PASSWORD", ""),
    "user_agent": "memzy-bot/1.0 (+github actions)",
    "subreddit": os.getenv("SUBREDDIT", "memzy"),
    "bot_username": os.getenv("BOT_USERNAME", ""),

    "welcome_enabled": env_bool("WELCOME_ENABLED", "true"),
    "flair_enabled": env_bool("FLAIR_ENABLED", "true"),
    "badges_enabled": env_bool("BADGES_ENABLED", "true"),
    "weekly_sticky_enabled": env_bool("WEEKLY_STICKY_ENABLED", "true"),
    

    "post_reward_thresholds": [
        int(x.strip()) for x in os.getenv("POST_REWARD_THRESHOLDS", "5,10,25,50").split(",") if x.strip().isdigit()
    ],

    "hot_take_score": int(os.getenv("HOT_TAKE_SCORE", "50")),
}
