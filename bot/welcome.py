WELCOME_MSG = (
    "Welcome to r/{sub}! 🎉\n\n"
    "Your first post has been detected.\n\n"
    "Keep posting — the weekly **Degenerate Leaderboard** rewards activity.\n"
    "_Bonus: comment more to unlock 🔥HotTake badges._"
)

def maybe_welcome(reddit, meta, post, subreddit_name):
    if post.id in meta.get("welcomed_posts", []):
        return False

    author = getattr(post.author, "name", None)
    if not author:
        return False

    if author.lower() == reddit.user.me().name.lower():
        return False

    body = WELCOME_MSG.format(sub=subreddit_name)

    try:
        post.reply(body)
        meta.setdefault("welcomed_posts", []).append(post.id)
        return True
    except Exception:
        return False
