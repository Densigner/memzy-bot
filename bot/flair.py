from bot.storage import load_counts

def build_flair_text(stats, thresholds, hot_take_score):
    base = f"P:{stats['posts']} • C:{stats['comments']} • 🔥{stats['streak']}"

    badge = ""
    for t in sorted(thresholds, reverse=True):
        if stats["posts"] >= t:
            if t >= 50:  badge = " 🏆"
            elif t >= 25: badge = " 🥇"
            elif t >= 10: badge = " 🥈"
            elif t >= 5:  badge = " 🥉"
            break

    if stats.get("comment_karma_in_sub", 0) >= hot_take_score:
        badge += " 🔥HotTake"

    return (base + badge).strip()

def update_user_flair(subreddit, username, thresholds, hot_take_score):
    data = load_counts()
    user = data["users"].get(username)
    if not user:
        return
    text = build_flair_text(user, thresholds, hot_take_score)
    subreddit.flair.set(username, text=text)
