# memzy-bot

This repository contains a small scaffold for the memzy-bot project.

Structure created:

- .github/workflows/memzy-bot-cron.yml — daily cron job
- .github/workflows/memzy-weekly.yml — weekly cron job
- bot/ — bot package with simple placeholders
- state/.gitkeep — keep the state folder in git
- requirements.txt

How to use locally

1. Create a virtual environment and install any dependencies (if you add them to requirements.txt):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the cron job locally:

```powershell
python -m bot.main --cron
```

3. Run the weekly job locally:

```powershell
python -m bot.main --weekly
```

Connecting this folder to GitHub

- Create a repo on GitHub and add a remote, or use `gh repo create` if you have the GitHub CLI installed.
- Commit and push the files.

Credentials / secrets

- Copy `.env.example` to `.env` and fill in the values for your Reddit app and bot account:

	- REDDIT_CLIENT_ID — iyAdTAq7SmKwdhSkBSiGkg
	- REDDIT_CLIENT_SECRET — from your Reddit app
	- REDDIT_USERNAME — bot account username (no u/)
	- REDDIT_PASSWORD — bot account password
	- SUBREDDIT — `memzy` (default)
	- BOT_USERNAME — usually same as `REDDIT_USERNAME`

The repository includes a `bot/credentials.py` helper which loads these values from the environment. Install `python-dotenv` if you want `.env` auto-loaded:

```powershell
pip install python-dotenv
```

Make sure `.env` is listed in `.gitignore` so you don't accidentally commit secrets.

