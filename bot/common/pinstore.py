"""Shared storage helpers for the bot. Stdlib only, used by every container.

Files (inside the git repo, so they are published):
  skill/pinterest-taste/data/pins.json      written only by the collector
  skill/pinterest-taste/data/analysis.json  written only by the analyst
Every write goes to a temp file and is renamed into place, so a reader
never sees a half-written file.

pins.json:
  {"pins": {"<id>": {"id", "url", "title", "categories": [], "queries": [],
                     "collected": "YYYY-MM-DD"}}}
analysis.json:
  {"categories": {"<cat>": {"analyzed": [ids], "last_run": iso, "runs": n}},
   "foundations": {"last_run": iso, "category_runs_since": n}}
"""
import json
import os
import re
from pathlib import Path

REPO = Path(os.environ.get("REPO_DIR", "/repo"))
SKILL = REPO / "skill" / "pinterest-taste"
DATA = SKILL / "data"
REFS = SKILL / "references"
PINS = DATA / "pins.json"
ANALYSIS = DATA / "analysis.json"
TOPICS = DATA / "topics.json"
STATE = Path(os.environ.get("STATE_DIR", "/state"))
THUMBS = STATE / "thumbs"

PIN_ID = re.compile(r"^\d{5,25}$")
CATEGORY = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def load_topics():
    cats = read_json(TOPICS, {"categories": []})["categories"]
    return [c for c in cats if CATEGORY.match(c.get("category", ""))]


def merge_batch(store, category, query, collected, pins):
    """Merge collected pins into an in-memory store. Returns ids that were new."""
    if not CATEGORY.match(category):
        raise ValueError(f"bad category {category!r}")
    table = store.setdefault("pins", {})
    new_ids = []
    for p in pins:
        pid = str(p.get("id", ""))
        if not PIN_ID.match(pid):
            continue
        rec = table.get(pid)
        if rec is None:
            rec = table[pid] = {
                "id": pid,
                "url": f"https://www.pinterest.com/pin/{pid}/",
                "title": clean_title(p.get("title")),
                "categories": [], "queries": [], "collected": collected,
            }
            new_ids.append(pid)
        if category not in rec["categories"]:
            rec["categories"].append(category)
        if query and query not in rec["queries"]:
            rec["queries"].append(query)
        if not rec["title"]:
            rec["title"] = clean_title(p.get("title"))
    return new_ids


def clean_title(s):
    s = re.sub(r"^This (may )?contains?:\s*", "", str(s or ""), flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:220]


def pending_for(category, store, analysis):
    """Pins in a category that have a thumbnail but haven't been analyzed yet."""
    done = set(analysis.get("categories", {}).get(category, {}).get("analyzed", []))
    out = []
    for pid, rec in store.get("pins", {}).items():
        if category in rec["categories"] and pid not in done and (THUMBS / f"{pid}.jpg").exists():
            out.append(pid)
    return sorted(out, key=lambda i: store["pins"][i].get("collected", ""))
