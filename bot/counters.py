from datetime import datetime
from dateutil import tz
from .storage import load_counts, save_counts

UK = tz.gettz("Europe/London")

def _today_uk():
    return datetime.now(tz=UK).date().isoformat()

def ensure_user(data, username):
    if username not in data["users"]:
        data["users"][username] = {
            "posts": 0,
            "comments": 0,
            "streak": 0,
            "last_active_day": None,
            "comment_karma_in_sub": 0,
            "first_post_id": None,
        }
    return data["users"][username]

def bump_activity(user):
    today = _today_uk()
    last = user["last_active_day"]

    if last is None:
        user["streak"] = 1
    else:
        last_dt = datetime.fromisoformat(last)
        today_dt = datetime.fromisoformat(today)
        if last_dt == today_dt:
            pass
        elif (today_dt - last_dt).days == 1:
            user["streak"] += 1
        else:
            user["streak"] = 1

    user["last_active_day"] = today

def record_submission(username, post_id):
    data = load_counts()
    u = ensure_user(data, username)
    u["posts"] += 1
    bump_activity(u)
    if u["first_post_id"] is None:
        u["first_post_id"] = post_id
    save_counts(data)

def record_comment(username, score_delta=0):
    data = load_counts()
    u = ensure_user(data, username)
    u["comments"] += 1
    try:
        u["comment_karma_in_sub"] += int(score_delta)
    except:
        pass
    bump_activity(u)
    save_counts(data)

def snapshot_top(n=10):
    data = load_counts()
    ranked = sorted(
        data["users"].items(),
        key=lambda kv: (
            kv[1]["posts"] + kv[1]["comments"],
            kv[1]["posts"],
            kv[1]["streak"],
        ),
        reverse=True,
    )
    return ranked[:n], data
