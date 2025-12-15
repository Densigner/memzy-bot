from bot.storage import load_counts

def pick_meme_lord():
    data = load_counts()

    ranked = sorted(
        data["users"].items(),
        key=lambda kv: (
            kv[1]["posts"] * 3 + kv[1]["comments"],
            kv[1]["streak"]
        ),
        reverse=True,
    )

    for username, stats in ranked:
        if stats["posts"] >= 30:
            return username, stats

    return None, None
