# pinterest-taste

A Claude Code skill that gives Claude a current, concrete sense of UI/UX taste: directions, palettes, type, layout and components distilled from thousands of Pinterest design pins. A bot keeps it refreshed.

It holds **patterns, not copies.** The repo stores pin links and Pinterest's alt-text only. No images are stored, and every pin belongs to its creator.

## Use the skill

```sh
git clone https://github.com/mjahidhasand/pinterest-taste.git
cd pinterest-taste
./install.sh            # macOS/Linux: links skill/pinterest-taste into ~/.claude/skills
# Windows: powershell -ExecutionPolicy Bypass -File install.ps1
```

Run `git pull` any time to get the latest patterns. Claude Code loads the skill automatically when you ask for a new UI. You can also say "use pinterest-taste".

To browse, open `skill/pinterest-taste/catalog.html` to see the collected pins by category, and `skill/pinterest-taste/references/` for the pattern files.

## How the bot works

```
collector ──pins.json + thumbnails──▶ analyst ──references/*.md──▶ publisher ──git push──▶ GitHub
(browser, paced)                      (Claude Code, Read/Edit/Write only)   (validates, deploy key)
```

- **collector**: a real Chromium on a virtual display. It rotates through the searches in `skill/pinterest-taste/data/topics.json`, with a 15–40 minute random gap between searches and at most 60 a day. It backs off for up to 12 h if Pinterest pushes back. It caches 474px thumbnails locally for the analyst; these are never pushed.
- **analyst**: when a category has 40 or more new pins, headless Claude Code looks at them and rewrites `references/<category>.md`. Every 6 category runs it re-synthesises `_foundations.md`. Claude gets no shell or web tools, can't read outside its workspace, and its output is validated.
- **publisher**: every 15 minutes it rebuilds the catalog and index, re-checks everything for secrets and stray links, then commits and pushes. It is the only container with the deploy key.

## Run the bot (on the VM)

```sh
cp .env.example .env    # then fill CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`) and DEPLOY_KEY_PATH
docker compose up -d --build
docker compose logs -f
```

**Log in once:** the collector waits until a Pinterest session exists. From your PC:

```sh
ssh -L 6080:localhost:6080 adv-devpc-002@10.20.1.41
```

Then open <http://localhost:6080/vnc.html>, click Connect, and log in to Pinterest with a spare account in the browser that appears. The session is saved in the `state` volume.

| Task | Command |
|---|---|
| Status | `docker compose exec collector cat /state/collector_status.json` |
| Tests | `docker run --rm -v "$PWD":/r -w /r python:3.12-slim python -m unittest discover -s bot/tests -v` |
| Add a topic | edit `data/topics.json`, then `docker compose restart collector` |
| Stop | `docker compose down` (the session and thumbnails are kept in volumes) |

## Respect

Pinterest's terms restrict automated collection. The bot runs slowly with one account, stores no images, and only publishes links back to the original pins. If you're a creator and want a pin removed from the references, open an issue.
