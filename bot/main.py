"""Entry point for memzy-bot (CLI for actions triggered by cron/workflows)."""
import argparse
from .config import BOT_NAME
from .counters import Counters
from .leaderboard import Leaderboard


def run_cron():
    print(f"Running cron job for {BOT_NAME}")
    # placeholder: implement daily actions
    c = Counters()
    c.increment('cron_runs')
    print('cron job completed')


def run_weekly():
    print(f"Running weekly job for {BOT_NAME}")
    lb = Leaderboard()
    print('Top entries:', lb.top_n(5))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cron', action='store_true')
    parser.add_argument('--weekly', action='store_true')
    args = parser.parse_args()

    if args.cron:
        run_cron()
    elif args.weekly:
        run_weekly()
    else:
        parser.print_help()
