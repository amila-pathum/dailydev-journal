import json
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API_URL = "https://zenquotes.io/api/random"

DATA_FILE = Path("site/data/quotes.json")

SRI_LANKA = ZoneInfo("Asia/Colombo")


def fetch_quote():
    """Fetch a random quote from ZenQuotes."""

    request = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "DailyDevJournal/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    if not isinstance(data, list) or not data:
        raise ValueError("Invalid API response")

    quote = data[0].get("q", "").strip()
    author = data[0].get("a", "").strip()

    if not quote or not author:
        raise ValueError("Quote or author is missing")

    return {
        "quote": quote,
        "author": author
    }


def load_history():
    """Load existing quote history."""

    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    """Save quote history."""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2, ensure_ascii=False)


def main():
    today = datetime.now(SRI_LANKA).date().isoformat()

    history = load_history()

    # Avoid multiple entries on the same day.
    if any(item["date"] == today for item in history):
        print("Today's quote already exists.")
        return

    quote = fetch_quote()

    entry = {
        "date": today,
        "quote": quote["quote"],
        "author": quote["author"]
    }

    history.append(entry)

    history.sort(key=lambda item: item["date"], reverse=True)

    save_history(history)

    print(f"Successfully saved quote for {today}")
    print(quote["quote"])
    print(f"Author: {quote['author']}")


if __name__ == "__main__":
    main()