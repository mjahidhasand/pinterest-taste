"""Commits and pushes skill updates. The only container holding the deploy key.

Every PUBLISH_EVERY_SEC: rebuild catalog.html and references/README.md, stage
skill/ only, re-validate every staged markdown file and scan everything staged
for secrets, then commit and push. Anything suspicious blocks the push and is
left unstaged for a human to look at.
"""
import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/app/common")
import pinstore as ps  # noqa: E402
from build_catalog import build  # noqa: E402
from validate import secret_findings, validate_reference  # noqa: E402

EVERY = int(os.environ.get("PUBLISH_EVERY_SEC", 900))
BRANCH = os.environ.get("GIT_BRANCH", "main")
ALLOWED_PREFIX = "skill/pinterest-taste/"


def log(msg):
    print(f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(ps.REPO), *args], capture_output=True, text=True, timeout=180)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()[-400:]}")
    return r.stdout


def staged_problems(paths, known_ids):
    problems = []
    for rel in paths:
        if not rel.startswith(ALLOWED_PREFIX):
            problems.append(f"{rel}: outside {ALLOWED_PREFIX}")
            continue
        path = ps.REPO / rel
        if not path.exists():
            continue  # deletion
        text = path.read_text(encoding="utf-8", errors="replace")
        if rel.endswith(".md") and "/references/" in rel and not rel.endswith("README.md"):
            category = not Path(rel).name.startswith("_")
            problems += [f"{rel}: {p}" for p in validate_reference(text, known_ids, category=category)]
        elif not rel.endswith(".json") or rel.endswith("pins.json"):
            # pins.json titles are free text from strangers: scan them too.
            problems += [f"{rel}: secret-like ({f})" for f in secret_findings(text) if f != "long opaque string"]
    return problems


def publish_once():
    build()
    git("add", "--", "skill/")
    paths = [p for p in git("diff", "--cached", "--name-only").splitlines() if p]
    if not paths:
        return "nothing to publish"
    store = ps.read_json(ps.PINS, {"pins": {}})
    problems = staged_problems(paths, set(store["pins"]))
    if problems:
        git("reset", "-q")
        return "BLOCKED: " + " | ".join(problems[:10])
    analysis = ps.read_json(ps.ANALYSIS, {"categories": {}})
    cats = sorted({Path(p).stem for p in paths if "/references/" in p and p.endswith(".md")} - {"README"})
    msg = f"bot: {len(store['pins'])} pins" + (f"; updated {', '.join(cats)}" if cats else "")
    git("commit", "-q", "-m", msg)
    git("pull", "-q", "--rebase", "origin", BRANCH)
    git("push", "-q", "origin", f"HEAD:{BRANCH}")
    return f"pushed: {msg} ({len(analysis.get('categories', {}))} categories analyzed)"


def main():
    git("config", "user.name", "pinterest-taste-bot")
    git("config", "user.email", "pinterest-taste-bot@users.noreply.github.com")
    while True:
        try:
            log(publish_once())
        except Exception as e:  # log and retry next cycle; never crash-loop the push
            log(f"publish error: {e}")
        time.sleep(EVERY)


if __name__ == "__main__":
    main()
