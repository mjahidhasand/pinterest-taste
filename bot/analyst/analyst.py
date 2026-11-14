"""Turns collected pins into pattern files with Claude Code (subscription auth).

Loop: every POLL_SEC, pick the category with the most unanalyzed pins. Run when
it has >= MIN_NEW pending, or >= MIN_STALE pending and no run for STALE_DAYS.
Claude works in a throwaway workspace with ONLY Read/Edit/Write, sees the
thumbnails + current reference, and rewrites reference.md. The result is
validated (validate.py) before it replaces references/<category>.md.
After FOUNDATIONS_EVERY category runs, it re-synthesises _foundations.md.

Pin titles and images are untrusted (anyone can post a pin), so: no shell or
web tools for Claude, reads outside the workspace denied, output validated,
and the publisher runs a second secret scan before anything is pushed.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, "/app/common")
import pinstore as ps  # noqa: E402
from validate import validate_reference  # noqa: E402

POLL_SEC = int(os.environ.get("ANALYST_POLL_SEC", 600))
MIN_NEW = int(os.environ.get("ANALYST_MIN_NEW", 40))
MIN_STALE = int(os.environ.get("ANALYST_MIN_STALE", 10))
STALE_DAYS = int(os.environ.get("ANALYST_STALE_DAYS", 7))
BATCH = int(os.environ.get("ANALYST_BATCH", 60))
FOUNDATIONS_EVERY = int(os.environ.get("FOUNDATIONS_EVERY", 6))
MODEL = os.environ.get("ANALYST_MODEL", "sonnet")
RUN_TIMEOUT = int(os.environ.get("ANALYST_RUN_TIMEOUT_SEC", 1800))
PROMPTS = Path("/app/prompts")
SETTINGS = Path("/app/claude-settings.json")


def log(msg):
    print(f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def pick_category(store, analysis):
    best = None
    for t in ps.load_topics():
        cat = t["category"]
        pending = ps.pending_for(cat, store, analysis)
        last = analysis.get("categories", {}).get(cat, {}).get("last_run")
        stale = last is None or (
            dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(last)
        ).days >= STALE_DAYS
        due = len(pending) >= MIN_NEW or (stale and len(pending) >= MIN_STALE)
        if due and (best is None or len(pending) > len(best[1])):
            best = (cat, pending)
    return best


def run_claude(workdir, prompt):
    """Run one headless Claude Code job. Returns (ok, short message)."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # never bill the API
    cmd = [
        "claude", "-p", prompt,
        "--model", MODEL,
        "--tools", "Read,Edit,Write",
        "--allowedTools", "Read,Edit,Write",
        "--permission-mode", "acceptEdits",
        "--settings", str(SETTINGS),
        "--max-turns", "80",
        "--output-format", "json",
    ]
    try:
        r = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True, timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if r.returncode != 0:
        return False, (r.stdout or r.stderr)[-500:]
    try:
        out = json.loads(r.stdout)
        if out.get("is_error"):
            return False, str(out.get("result", ""))[-500:]
    except json.JSONDecodeError:
        pass
    return True, "ok"


def analyze_category(cat, pending, store, analysis):
    batch = pending[:BATCH]
    ref_path = ps.REFS / f"{cat}.md"
    with tempfile.TemporaryDirectory(prefix=f"analyze-{cat}-") as tmp:
        w = Path(tmp)
        (w / "pins").mkdir()
        rows = []
        for pid in batch:
            shutil.copy(ps.THUMBS / f"{pid}.jpg", w / "pins" / f"{pid}.jpg")
            rows.append({"id": pid, "url": store["pins"][pid]["url"], "title": store["pins"][pid]["title"]})
        (w / "pins.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
        if ref_path.exists():
            shutil.copy(ref_path, w / "reference.md")
        prompt = (PROMPTS / "category.md").read_text(encoding="utf-8").replace("{{CATEGORY}}", cat).replace(
            "{{TODAY}}", dt.date.today().isoformat()).replace("{{N}}", str(len(batch)))
        ok, msg = run_claude(w, prompt)
        if not ok:
            return False, msg
        out = w / "reference.md"
        if not out.exists():
            return False, "Claude did not write reference.md"
        text = out.read_text(encoding="utf-8")
        known_ids = set(store["pins"])
        problems = validate_reference(text, known_ids, category=True)
        if problems:
            return False, "validation: " + "; ".join(problems)
        ps.REFS.mkdir(parents=True, exist_ok=True)
        tmp_ref = ref_path.with_name(ref_path.name + ".tmp")
        tmp_ref.write_text(text, encoding="utf-8")
        os.replace(tmp_ref, ref_path)

    entry = analysis.setdefault("categories", {}).setdefault(cat, {"analyzed": [], "runs": 0})
    entry["analyzed"] = sorted(set(entry["analyzed"]) | set(batch))
    entry["last_run"] = now()
    entry["runs"] += 1
    f = analysis.setdefault("foundations", {"category_runs_since": 0})
    f["category_runs_since"] = f.get("category_runs_since", 0) + 1
    ps.write_json(ps.ANALYSIS, analysis)
    return True, f"{len(batch)} pins"


def synthesize_foundations(store, analysis):
    refs = sorted(p for p in ps.REFS.glob("*.md") if not p.name.startswith("_") and p.name != "README.md")
    if len(refs) < 3:
        return False, "fewer than 3 category files"
    with tempfile.TemporaryDirectory(prefix="foundations-") as tmp:
        w = Path(tmp)
        (w / "categories").mkdir()
        for r in refs:
            shutil.copy(r, w / "categories" / r.name)
        current = ps.REFS / "_foundations.md"
        if current.exists():
            shutil.copy(current, w / "foundations.md")
        prompt = (PROMPTS / "foundations.md").read_text(encoding="utf-8").replace(
            "{{TODAY}}", dt.date.today().isoformat())
        ok, msg = run_claude(w, prompt)
        if not ok:
            return False, msg
        out = w / "foundations.md"
        if not out.exists():
            return False, "Claude did not write foundations.md"
        text = out.read_text(encoding="utf-8")
        problems = validate_reference(text, set(store["pins"]), category=False)
        if problems:
            return False, "validation: " + "; ".join(problems)
        tmp_ref = current.with_name(current.name + ".tmp")
        tmp_ref.write_text(text, encoding="utf-8")
        os.replace(tmp_ref, current)
    analysis["foundations"] = {"last_run": now(), "category_runs_since": 0}
    ps.write_json(ps.ANALYSIS, analysis)
    return True, f"{len(refs)} categories"


def main():
    if not os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        log("CLAUDE_CODE_OAUTH_TOKEN is not set (run `claude setup-token` and put it in .env); waiting")
    backoff = 0
    while True:
        if not os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
            time.sleep(POLL_SEC)
            continue
        store = ps.read_json(ps.PINS, {"pins": {}})
        analysis = ps.read_json(ps.ANALYSIS, {"categories": {}, "foundations": {"category_runs_since": 0}})
        ok = True
        if analysis.get("foundations", {}).get("category_runs_since", 0) >= FOUNDATIONS_EVERY:
            ok, msg = synthesize_foundations(store, analysis)
            log(f"foundations: {'updated' if ok else 'FAILED'} ({msg})")
        else:
            choice = pick_category(store, analysis)
            if choice:
                cat, pending = choice
                log(f"[{cat}] analyzing {min(len(pending), BATCH)} of {len(pending)} pending pins")
                ok, msg = analyze_category(cat, pending, store, analysis)
                log(f"[{cat}] {'updated' if ok else 'FAILED'} ({msg})")
        # Previews are only kept until every category that needs them has analyzed them.
        removed = ps.prune_thumbs(store, ps.read_json(ps.ANALYSIS, {"categories": {}}))
        if removed:
            log(f"deleted {removed} analyzed previews")
        if ok:
            backoff = 0
            time.sleep(POLL_SEC)
        else:
            # Usage limits, outages and bad output all land here: back off, never hammer.
            backoff = min(6 * 3600, max(1800, backoff * 2))
            log(f"backing off {backoff // 60} min")
            time.sleep(backoff)


if __name__ == "__main__":
    main()
