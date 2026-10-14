"""Baixa o calendário público de contribuições (sem token) e salva data/contributions.json.

Uso: python scripts/fetch_contributions.py [usuario]
"""

import json
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "LucasfNeves"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch_days(username: str) -> list[dict]:
    resp = requests.get(
        f"https://github.com/users/{username}/contributions",
        headers={"User-Agent": "profile-readme-bot"},
        timeout=30,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    counts: dict[str, int] = {}
    for tip in soup.select("tool-tip"):
        target = tip.get("for")
        m = re.match(r"\s*(\d+|No) contribution", tip.get_text())
        if target and m:
            counts[target] = 0 if m.group(1) == "No" else int(m.group(1))

    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({
            "date": cell["data-date"],
            "level": int(cell.get("data-level", 0)),
            "count": counts.get(cell.get("id", ""), 0),
        })
    days.sort(key=lambda d: d["date"])
    if not days:
        raise SystemExit("Nenhum dia encontrado — o HTML do GitHub pode ter mudado.")
    return days


def stats(days: list[dict]) -> dict:
    total = sum(d["count"] for d in days)
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif current == 0 and d is days[-1]:
            continue  # hoje ainda sem commit não quebra a sequência
        else:
            break

    best = max(days, key=lambda d: d["count"])
    monthly = defaultdict(int)
    for d in days:
        monthly[d["date"][:7]] += d["count"]
    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": dict(sorted(monthly.items())),
    }


def main() -> None:
    days = fetch_days(USERNAME)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"username": USERNAME, "days": days, "stats": stats(days)}, indent=1), encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parent.parent)} ({len(days)} dias)")


if __name__ == "__main__":
    main()
