"""Always-on, paced Pinterest collector.

Cycles through every (category, query) in topics.json forever. For each search
it scrolls the results, records pin id/url/alt text into pins.json and caches a
474px thumbnail in /state/thumbs (thumbnails are NOT published; the analyst
reads them, then they stay local).

Pacing (env): MIN_GAP_MIN / MAX_GAP_MIN minutes between searches,
MAX_SEARCHES_PER_DAY, SCROLL_ROUNDS. Pushback from Pinterest (login wall,
"unusual activity", empty results) triggers exponential backoff up to 12 h.

Login: the browser runs on a virtual display you can open through noVNC
(see README). Log in once with a spare account; the profile lives in /state.
"""
import asyncio
import datetime as dt
import json
import os
import random
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

sys.path.insert(0, "/app/common")
import pinstore as ps  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

MIN_GAP = float(os.environ.get("MIN_GAP_MIN", 15))
MAX_GAP = float(os.environ.get("MAX_GAP_MIN", 40))
MAX_PER_DAY = int(os.environ.get("MAX_SEARCHES_PER_DAY", 60))
ROUNDS = int(os.environ.get("SCROLL_ROUNDS", 12))
MAX_THUMBS = int(os.environ.get("MAX_THUMBS_PER_SEARCH", 150))
PROFILE = ps.STATE / "profile"
STATUS = ps.STATE / "collector_status.json"

# Runs inside the page. Pinterest virtualises the grid, so read it on every
# scroll step and accumulate by id. Promoted pins (ads) are skipped.
COLLECT_JS = """
async (rounds) => {
  const seen = new Map();
  for (let i = 0; i < rounds; i++) {
    document.querySelectorAll('div[data-test-id="pin"], div[data-grid-item="true"]').forEach((el) => {
      const a = el.querySelector('a[href*="/pin/"]');
      const img = el.querySelector('img');
      const id = a?.getAttribute('href')?.match(/\\/pin\\/(\\d+)/)?.[1];
      if (!id || seen.has(id)) return;
      if (/\\bPromoted\\b|\\bSponsored\\b/i.test(el.innerText || '')) return;
      seen.set(id, { id, title: img?.alt || '', src: img?.currentSrc || img?.src || '' });
    });
    window.scrollBy(0, Math.round(window.innerHeight * 1.8));
    await new Promise((r) => setTimeout(r, 1200 + Math.random() * 900));
  }
  return [...seen.values()];
}
"""


def log(msg):
    print(f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def status(**kw):
    cur = ps.read_json(STATUS, {})
    cur.update(kw, updated=dt.datetime.now().isoformat(timespec="seconds"))
    ps.write_json(STATUS, cur)


def thumb_url(src):
    # i.pinimg.com/236x/aa/bb/cc/hash.jpg -> 474x is legible for analysis and still small.
    if "i.pinimg.com/" not in src:
        return None
    parts = src.split("/")
    if len(parts) > 3:
        parts[3] = "474x"
    return "/".join(parts)


async def logged_in(ctx):
    cookies = await ctx.cookies("https://www.pinterest.com")
    return any(c["name"] == "_auth" and c["value"] == "1" for c in cookies)


async def blocked(page):
    if "/login" in page.url or "/challenge" in page.url:
        return True
    text = (await page.inner_text("body"))[:5000].lower()
    return any(s in text for s in ("unusual activity", "verify you are human", "too many requests"))


async def search(page, ctx, category, query):
    url = f"https://www.pinterest.com/search/pins/?q={quote_plus(query)}&rs=typed"
    await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    await page.wait_for_timeout(4000)
    if await blocked(page):
        return None
    found = await page.evaluate(COLLECT_JS, ROUNDS)
    store = ps.read_json(ps.PINS, {"pins": {}})
    new_ids = ps.merge_batch(store, category, query, dt.date.today().isoformat(), found)
    ps.write_json(ps.PINS, store)

    ps.THUMBS.mkdir(parents=True, exist_ok=True)
    got = 0
    by_id = {p["id"]: p for p in found}
    for pid in new_ids[:MAX_THUMBS]:
        dest = ps.THUMBS / f"{pid}.jpg"
        src = thumb_url(by_id[pid].get("src", ""))
        if dest.exists() or not src:
            continue
        try:
            r = await ctx.request.get(src, timeout=30_000)
            if r.ok and r.headers.get("content-type", "").startswith("image/"):
                dest.write_bytes(await r.body())
                got += 1
        except Exception as e:  # one bad image must not stop the run
            log(f"thumb {pid} failed: {e}")
        await asyncio.sleep(random.uniform(0.4, 1.2))
    return len(found), len(new_ids), got


async def main():
    topics = ps.load_topics()
    jobs = [(t["category"], q) for t in topics for q in t["queries"]]
    log(f"{len(jobs)} searches in rotation; gap {MIN_GAP}-{MAX_GAP} min; cap {MAX_PER_DAY}/day")
    backoff_h = 0
    day, done_today = dt.date.today(), 0

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            str(PROFILE), headless=False, viewport={"width": 1440, "height": 900}, locale="en-US",
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        while True:
            random.shuffle(jobs)
            for category, query in jobs:
                if dt.date.today() != day:
                    day, done_today = dt.date.today(), 0
                if done_today >= MAX_PER_DAY:
                    status(state="daily_cap", searches_today=done_today)
                    log("daily cap reached; sleeping until tomorrow")
                    while dt.date.today() == day:
                        await asyncio.sleep(600)
                    day, done_today = dt.date.today(), 0

                if not await logged_in(ctx):
                    status(state="login_required")
                    log("not logged in - open noVNC and log in with the spare account")
                    await page.goto("https://www.pinterest.com/login/", wait_until="domcontentloaded")
                    while not await logged_in(ctx):
                        await asyncio.sleep(30)
                    log("login detected")

                try:
                    result = await search(page, ctx, category, query)
                except Exception as e:
                    log(f"search '{query}' error: {e}")
                    result = (0, 0, 0)
                done_today += 1

                if result is None or result[0] == 0:
                    backoff_h = min(12, max(1, backoff_h * 2))
                    status(state="backoff", backoff_hours=backoff_h, last_query=query)
                    log(f"pushback on '{query}'; backing off {backoff_h} h")
                    await asyncio.sleep(backoff_h * 3600)
                    continue
                backoff_h = 0
                seen, new, thumbs = result
                total = len(ps.read_json(ps.PINS, {"pins": {}})["pins"])
                status(state="ok", last_query=query, last_category=category, last_seen=seen,
                       last_new=new, last_thumbs=thumbs, total_pins=total, searches_today=done_today)
                log(f"[{category}] '{query}': {seen} seen, {new} new, {thumbs} thumbs, {total} total")
                await asyncio.sleep(random.uniform(MIN_GAP, MAX_GAP) * 60)


if __name__ == "__main__":
    asyncio.run(main())
