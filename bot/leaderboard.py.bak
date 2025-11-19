"""Leaderboard utilities (placeholder)."""
import praw
from .config import CONFIG
from .storage import load_meta, save_meta
from .counters import snapshot_top

def main():
    reddit = praw.Reddit(
        client_id=CONFIG["client_id"],
        client_secret=CONFIG["client_secret"],
        username=CONFIG["username"],
        password=CONFIG["password"],
        user_agent=CONFIG["user_agent"],
    )
    sub = reddit.subreddit(CONFIG["subreddit"])

    top, data = snapshot_top(10)

    if not top:
        return

    lines = [
        "# 🏁 Degenerate Leaderboard (This Week)",
        "",
        "| Rank | User | Posts | Comments | Streak |",
        "|---:|:-----|---:|---:|---:|"
    ]

    for i, (u, s) in enumerate(top, start=1):
        lines.append(
            f"| {i} | u/{u} | {s['posts']} | {s['comments']} | {s['streak']} |"
        )

    body = "\n".join(lines)
    title = "Degenerate Leaderboard — Weekly Rankings"

    post = sub.submit(title=title, selftext=body, send_replies=False)

    try:
        post.mod.sticky()
    except:
        pass

    meta = load_meta()
    meta.setdefault("weekly_threads", {})["leaderboard_post_id"] = post.id
    save_meta(meta)

if __name__ == "__main__":
    main()
