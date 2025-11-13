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

