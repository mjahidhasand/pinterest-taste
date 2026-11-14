"""Checks generated markdown before it is saved (analyst) and pushed (publisher).

The model reads untrusted pins, so its output is untrusted too. A file is
rejected when it is too large, misses required sections, links anywhere but
Pinterest pins we actually collected, or contains anything secret-shaped.
"""
import re

MAX_BYTES = 60_000
CATEGORY_SECTIONS = ("## Directions", "## Do / Don't", "## Source pins")
FOUNDATIONS_SECTIONS = ("## Principles", "## Choosing a direction")

URL = re.compile(r"https?://[^\s)\]>\"']+", re.I)
PIN_URL = re.compile(r"^https://www\.pinterest\.com/pin/(\d{5,25})/?$")
SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}"),
    re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(xox[abposr]-[A-Za-z0-9-]{10,})"),
    re.compile(r"CLAUDE_CODE_OAUTH_TOKEN|ANTHROPIC_API_KEY"),
    re.compile(r"/proc/|/run/secrets|\.credentials\.json"),
]
# Long unbroken runs of token-ish characters (hex colors and pin ids are short).
OPAQUE = re.compile(r"[A-Za-z0-9+/=_-]{48,}")


def secret_findings(text):
    found = [p.pattern for p in SECRET_PATTERNS if p.search(text)]
    if OPAQUE.search(text):
        found.append("long opaque string")
    return found


def validate_reference(text, known_pin_ids, category=True):
    problems = []
    if len(text.encode("utf-8")) > MAX_BYTES:
        problems.append(f"larger than {MAX_BYTES} bytes")
    for section in CATEGORY_SECTIONS if category else FOUNDATIONS_SECTIONS:
        if section not in text:
            problems.append(f"missing section '{section}'")
    for url in URL.findall(text):
        m = PIN_URL.match(url)
        if not m:
            problems.append(f"non-pin link {url[:80]}")
        elif m.group(1) not in known_pin_ids:
            problems.append(f"unknown pin {m.group(1)}")
    if "<script" in text.lower() or "<iframe" in text.lower():
        problems.append("embedded HTML script/iframe")
    problems += [f"secret-like content ({f})" for f in secret_findings(text)]
    return problems[:20]
