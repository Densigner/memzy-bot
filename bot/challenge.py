import random
import praw
from bot.config import CONFIG
from bot.storage import load_meta, save_meta

CHALLENGES = [
    "📱 Phone-in-hand POV — caption your most cursed notification.",
    "🖼️ Classic painting — insert modern UI popups.",
    "🍞 Toast That — turn boring objects into epic revelations.",
    "🎮 Patch Notes — write life as a game update.",
    "📈 Doom Graph — create absurd graphs portraying 'facts'.",
]

def main():
    if not CONFIG["weekly_challenge_enabled"]:
        return

    reddit = praw.Reddit(
        client_id=CONFIG["client_id"],
        client_secret=CONFIG["client_secret"],
        username=CONFIG["username"],
        password=CONFIG["password"],
        user_agent=CONFIG["user_agent"],
    )
    sub = reddit.subreddit(CONFIG["subreddit"])

    prompt = random.choice(CHALLENGES)

    title = "🔥 Weekly Meme Challenge"
    body = f"{prompt}\n\nPost with flair **Challenge** and we’ll feature the best ones."

    post = sub.submit(title=title, selftext=body, send_replies=False)

    try:
        post.mod.sticky(bottom=True)
    except:
        pass

    meta = load_meta()
    meta.setdefault("weekly_threads", {})["challenge_post_id"] = post.id
    save_meta(meta)

if __name__ == "__main__":
    main()
