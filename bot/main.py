import time
import praw

from bot.config import CONFIG
from bot.storage import load_meta, save_meta
from bot.counters import record_submission, record_comment
from bot.flair import update_user_flair

WINDOW_MINUTES = 15


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

    # --- dedupe state (JSON-safe) ---
    meta.setdefault("seen_posts", [])
    meta.setdefault("seen_comments", [])

    seen_posts = set(meta["seen_posts"])
    seen_comments = set(meta["seen_comments"])

    cutoff = time.time() - WINDOW_MINUTES * 60

    # -------------------------
    # Submissions
    # -------------------------
    for post in sub.new(limit=100):
        if post.created_utc < cutoff:
            break

        author = getattr(post.author, "name", None)
        if not author:
            continue

        if post.id in seen_posts:
            continue

        record_submission(author, post.id)
        seen_posts.add(post.id)

        if CONFIG["flair_enabled"]:
            try:
                update_user_flair(
                    sub,
                    author,
                    CONFIG["post_reward_thresholds"],
                    CONFIG["hot_take_score"],
                )
            except Exception:
                pass

    # -------------------------
    # Comments
    # -------------------------
    for c in sub.comments(limit=200):
        if c.created_utc < cutoff:
            break

        author = getattr(c.author, "name", None)
        if not author or author.lower() == me:
            continue

        if c.id in seen_comments:
            continue

        score = getattr(c, "score", 0) or 0

        record_comment(author, score_delta=score)
        seen_comments.add(c.id)

        if CONFIG["flair_enabled"]:
            try:
                update_user_flair(
                    sub,
                    author,
                    CONFIG["post_reward_thresholds"],
                    CONFIG["hot_take_score"],
                )
            except Exception:
                pass

    # --- persist dedupe state ---
    meta["seen_posts"] = list(seen_posts)
    meta["seen_comments"] = list(seen_comments)

    save_meta(meta)


if __name__ == "__main__":
    main()
