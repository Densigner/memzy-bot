import time
import praw
from .config import CONFIG
from .storage import load_meta, save_meta
from .counters import record_submission, record_comment
from .flair import update_user_flair
from .welcome import maybe_welcome

WINDOW_MINUTES = 15

def main():
    reddit = praw.Reddit(
        client_id=CONFIG["client_id"],
        client_secret=CONFIG["client_secret"],
        username=CONFIG["username"],
        password=CONFIG["password"],
        user_agent=CONFIG["user_agent"],
    )

    sub = reddit.subreddit(CONFIG["subreddit"])
    me = reddit.user.me().name.lower()

    meta = load_meta()
    cutoff = time.time() - WINDOW_MINUTES * 60

    # Submissions
    for post in sub.new(limit=100):
        if post.created_utc < cutoff:
            break

        author = getattr(post.author, "name", None)
        if not author:
            continue

        record_submission(author, post.id)

        if CONFIG["welcome_enabled"]:
            if maybe_welcome(reddit, meta, post, CONFIG["subreddit"]):
                save_meta(meta)

        if CONFIG["flair_enabled"]:
            try:
                update_user_flair(
                    sub,
                    author,
                    CONFIG["post_reward_thresholds"],
                    CONFIG["hot_take_score"],
                )
            except:
                pass

    # Comments
    for c in sub.comments(limit=200):
        if c.created_utc < cutoff:
            break

        author = getattr(c.author, "name", None)
        if not author or author.lower() == me:
            continue

        score = getattr(c, "score", 0) or 0

        record_comment(author, score_delta=score)

        if CONFIG["flair_enabled"]:
            try:
                update_user_flair(
                    sub,
                    author,
                    CONFIG["post_reward_thresholds"],
                    CONFIG["hot_take_score"],
                )
            except:
                pass

    save_meta(meta)

if __name__ == "__main__":
    main()
