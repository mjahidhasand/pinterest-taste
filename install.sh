#!/bin/sh
# Link the skill into Claude Code. `git pull` then keeps it current.
set -eu
src="$(cd "$(dirname "$0")" && pwd)/skill/pinterest-taste"
mkdir -p "$HOME/.claude/skills"
ln -sfn "$src" "$HOME/.claude/skills/pinterest-taste"
echo "linked $HOME/.claude/skills/pinterest-taste -> $src"
