import time
import praw

from bot.config import CONFIG
from bot.storage import load_meta, save_meta
from bot.counters import record_submission, record_comment
from bot.flair import update_user_flair

# -------------------------
# CONFIG
# -------------------------
WINDOW_MINUTES = 120  # safe window for cron-based runs


def main():
    reddit = praw.Reddit(
        client_id=CONFIG["client_id"],
        client_secret=CONFIG["client_secret"],
        refresh_token=CONFIG["refresh_token"],
        user_agent=CONFIG["user_agent"],
    )

    sub = reddit.subreddit(CONFIG["subreddit"])
    me = reddit.user.me().name.lower()

    meta = load_meta()

    # -------------------------
    # DEDUPE STATE (JSON-safe)
    # -------------------------
    meta.setdefault("seen_posts", [])
    meta.setdefault("seen_comments", [])

    seen_posts = set(meta["seen_posts"])
    seen_comments = set(meta["seen_comments"])

    cutoff = time.time() - WINDOW_MINUTES * 60

    # -------------------------
    # SUBMISSIONS
    # -------------------------
    for post in sub.new(limit=100):
        if post.created_utc < cutoff:
            break  # submissions ARE ordered newest-first

        author = getattr(post.author, "name", None)
        if not author:
            continue

        if post.id in seen_posts:
            continue

        record_submission(author, post.id)
        seen_posts.add(post.id)

        if CONFIG.get("flair_enabled"):
            try:
                update_user_flair(
                    sub,
                    author,
                    CONFIG["post_reward_thresholds"],
                    CONFIG["hot_take_score"],
                )
            except Exception as e:
                print(f"[FLAIR ERROR][POST] {author}: {e}")

    # -------------------------
    # COMMENTS
    # -------------------------
    for c in sub.comments(limit=200):
        # IMPORTANT:
        # sub.comments() is NOT guaranteed to be ordered
        # so we must CONTINUE, not BREAK
        if c.created_utc < cutoff:
            continue

        author = getattr(c.author, "name", None)
        if not author or author.lower() == me:
            continue

        if c.id in seen_comments:
            continue

        # Record participation (NOT score)
        record_comment(author, score_delta=1)
        seen_comments.add(c.id)

        if CONFIG.get("flair_enabled"):
            try:
                update_user_flair(
                    sub,
                    author,
                    CONFIG["post_reward_thresholds"],
                    CONFIG["hot_take_score"],
                )
            except Exception as e:
                print(f"[FLAIR ERROR][COMMENT] {author}: {e}")

    # -------------------------
    # PERSIST DEDUPE STATE
    # -------------------------
    meta["seen_posts"] = list(seen_posts)
    meta["seen_comments"] = list(seen_comments)

    save_meta(meta)


if __name__ == "__main__":
    main()
