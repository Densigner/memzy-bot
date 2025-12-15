import praw
from bot.config import CONFIG
from bot.storage import load_meta, save_meta, load_counts
from bot.flair import build_flair_text

def pick_meme_lord():
    data = load_counts()

    ranked = sorted(
        data["users"].items(),
        key=lambda kv: (
            kv[1]["posts"] * 3 + kv[1]["comments"],
            kv[1]["streak"],
        ),
        reverse=True,
    )

    for username, stats in ranked:
        if stats["posts"] >= 30:
            return username, stats

    return None, None


def main():
    reddit = praw.Reddit(
        client_id=CONFIG["client_id"],
        client_secret=CONFIG["client_secret"],
        refresh_token=CONFIG["refresh_token"],
        user_agent=CONFIG["user_agent"],
    )

    sub = reddit.subreddit(CONFIG["subreddit"])
    meta = load_meta()
    meta.setdefault("ceremony", {})

    last_winner = meta["ceremony"].get("last_winner")

    winner, stats = pick_meme_lord()
    if not winner:
        return  # no eligible Meme Lord yet

    # -----------------------------
    # STEP 3: Restore last winner
    # -----------------------------
    if last_winner and last_winner != winner:
        normal_flair = build_flair_text(stats, CONFIG["hot_take_score"])
        try:
            sub.flair.set(last_winner, text=normal_flair)
        except:
            pass

    # -----------------------------
    # STEP 3: Apply ceremonial flair
    # -----------------------------
    ceremonial_text = ":memelord: Meme Lord of the Week"
    sub.flair.set(winner, text=ceremonial_text)

    # -----------------------------
    # STEP 4: Post ceremony thread
    # -----------------------------
    title = "🏛️ MEME LORD CEREMONY — This Week"
    body = f"""
🏛️ **MEME LORD CEREMONY**

After careful observation of crimes against decency,
the Scroll Gods have spoken.

👑 **Meme Lord of the Week**
u/{winner}

📊 **Stats**
• Posts: {stats['posts']}
• Comments: {stats['comments']}
• Streak: {stats['streak']}

The crown will pass next week.
Enjoy it while it lasts.
"""

    post = sub.submit(title=title, selftext=body, send_replies=False)

    try:
        post.mod.distinguish(sticky=True)
        post.mod.sticky()
    except:
        pass

    # -----------------------------
    # Save ceremony state
    # -----------------------------
    meta["ceremony"]["last_winner"] = winner
    meta["ceremony"]["last_post_id"] = post.id
    save_meta(meta)


if __name__ == "__main__":
    main()
