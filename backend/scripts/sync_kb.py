"""Download the latest KB articles from the helpdesk-kb repository into data/kb/."""

import json
import urllib.request
from pathlib import Path

REPO = "lucaswsanchez/helpdesk-kb"
DEST = Path(__file__).resolve().parent.parent / "data" / "kb"


def main() -> None:
    api = f"https://api.github.com/repos/{REPO}/contents/docs/kb"
    with urllib.request.urlopen(api, timeout=30) as res:
        entries = json.load(res)
    names = [
        e["name"] for e in entries if e["name"].startswith("kb-") and e["name"].endswith(".md")
    ]
    DEST.mkdir(parents=True, exist_ok=True)
    for name in names:
        url = f"https://raw.githubusercontent.com/{REPO}/main/docs/kb/{name}"
        with urllib.request.urlopen(url, timeout=30) as res:
            (DEST / name).write_bytes(res.read())
        print("synced", name)


if __name__ == "__main__":
    main()
