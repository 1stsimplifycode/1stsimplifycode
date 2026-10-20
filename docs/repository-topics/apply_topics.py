#!/usr/bin/env python3
"""Review and add GitHub repository topics (never delete existing topics)."""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "proposed-topics.json").read_text(encoding="utf-8"))
OWNER = DATA["owner"]

def token():
    value = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if value:
        return value
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit("No authentication. Install gh and run 'gh auth login' or set GH_TOKEN to an authorized token.")

def request(name, method, auth, body=None):
    url = f"https://api.github.com/repos/{OWNER}/{name}/topics"
    headers = {"Authorization": f"Bearer {auth}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "topic-curator"}
    raw = None if body is None else json.dumps({"names": body}).encode("utf-8")
    if raw is not None:
        headers["Content-Type"] = "application/json"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=raw, headers=headers, method=method), timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:350]
        raise RuntimeError(f"{method} {OWNER}/{name}: HTTP {exc.code}: {detail}") from exc

def main():
    ap = argparse.ArgumentParser(description="Add curated topics while preserving current topics")
    ap.add_argument("--apply", action="store_true", help="Actually change GitHub topics (default: dry-run)")
    ap.add_argument("--repo", help="Limit to one repository name")
    args = ap.parse_args()
    chosen = DATA["repositories"]
    if args.repo:
        if args.repo not in chosen:
            ap.error(f"Repository not in manifest: {args.repo}")
        chosen = {args.repo: chosen[args.repo]}
    auth = token()
    failures = 0
    for name, proposal in chosen.items():
        try:
            current = request(name, "GET", auth).get("names", [])
            merged = list(dict.fromkeys(current + proposal))
            if len(merged) > 20:
                print(f"SKIP {name}: {len(merged)} topics would exceed GitHub's 20-topic limit", file=sys.stderr)
                failures += 1
                continue
            print(f"{'APPLY' if args.apply else 'PREVIEW'} {name}: current={current} additions={[x for x in merged if x not in current]}")
            if args.apply and merged != current:
                request(name, "PUT", auth, merged)
        except Exception as exc:
            failures += 1
            print(f"ERROR {name}: {exc}", file=sys.stderr)
    print(f"Processed {len(chosen)}; errors/skips {failures}; mode={'APPLY' if args.apply else 'DRY RUN'}")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
