#!/usr/bin/env python3
"""Drain the private inbox repo (personal-feed) into the blog's content/.

Copies complete bundles (dirs containing index.md) from the inbox's micro/ and
stories/ folders into content/micro|stories/, then deletes them from the inbox
and pushes, so each item is intaken exactly once. The blog-repo commit of the
new content is done by the workflow after this script runs.

Env:
  INBOX_REPO   "owner/name" (default rishikeshsreehari/personal-feed)
  INBOX_PAT    PAT with read+write to the inbox repo
"""
import os
import shutil
import subprocess
import sys
import tempfile

INBOX_REPO = os.environ.get("INBOX_REPO", "rishikeshsreehari/personal-feed")
PAT = os.environ.get("INBOX_PAT")
CONTENT = os.path.join(os.getcwd(), "content")
COFFEE_FILE = os.path.join(os.getcwd(), "data", "coffee.txt")
SECTIONS = ("micro", "stories")


def drain_coffee(tmp, moved):
    """Append coffee/<ts>/brew.txt bundles to data/coffee.txt (coffee.txt format).

    Unlike micro/stories (one bundle -> one content dir), every coffee brew is a
    block appended to a single file. Bundle dirs are added to `moved` so the
    caller deletes them from the inbox after a successful append.
    """
    src_section = os.path.join(tmp, "coffee")
    if not os.path.isdir(src_section):
        return
    blocks = []
    for name in sorted(os.listdir(src_section)):
        src = os.path.join(src_section, name)
        if not os.path.isdir(src):
            continue
        brew = os.path.join(src, "brew.txt")
        if not os.path.exists(brew):
            print(f"skip incomplete coffee/{name}")
            continue
        with open(brew, encoding="utf-8") as fh:
            block = fh.read().strip()
        if block:
            blocks.append(block)
            print(f"intake coffee/{name}")
        moved.append(src)
    if not blocks:
        return
    existing = ""
    if os.path.exists(COFFEE_FILE):
        with open(COFFEE_FILE, encoding="utf-8") as fh:
            existing = fh.read()
    parts = [existing.rstrip()] if existing.strip() else []
    parts.extend(blocks)
    os.makedirs(os.path.dirname(COFFEE_FILE), exist_ok=True)
    with open(COFFEE_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n\n".join(parts).rstrip() + "\n")


def run(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check)


def main():
    if not PAT:
        print("INBOX_PAT not set — skipping intake.")
        return
    tmp = tempfile.mkdtemp(prefix="inbox-")
    url = f"https://x-access-token:{PAT}@github.com/{INBOX_REPO}.git"
    try:
        run(["git", "clone", "--depth", "1", url, tmp])
    except subprocess.CalledProcessError:
        print("Could not clone inbox (empty or unreachable) — nothing to intake.")
        shutil.rmtree(tmp, ignore_errors=True)
        return

    moved = []
    for section in SECTIONS:
        src_section = os.path.join(tmp, section)
        if not os.path.isdir(src_section):
            continue
        for name in sorted(os.listdir(src_section)):
            src = os.path.join(src_section, name)
            if not os.path.isdir(src):
                continue
            if not os.path.exists(os.path.join(src, "index.md")):
                print(f"skip incomplete {section}/{name}")
                continue
            dst = os.path.join(CONTENT, section, name)
            if os.path.exists(dst):
                print(f"already in blog, draining only: {section}/{name}")
            else:
                shutil.copytree(src, dst)
                print(f"intake {section}/{name}")
            moved.append(src)

    drain_coffee(tmp, moved)

    if not moved:
        print("nothing to intake")
        shutil.rmtree(tmp, ignore_errors=True)
        return

    for src in moved:
        shutil.rmtree(src, ignore_errors=True)

    run(["git", "config", "user.name", "GitHub Actions"], cwd=tmp)
    run(["git", "config", "user.email", "actions@github.com"], cwd=tmp)
    run(["git", "add", "-A"], cwd=tmp)
    # commit may be empty only if something odd happened; tolerate it
    subprocess.run(["git", "commit", "-m", "drain: intaken to blog"], cwd=tmp, check=False)
    run(["git", "push", "origin", "HEAD"], cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"intaken {len(moved)} item(s)")


if __name__ == "__main__":
    sys.exit(main())
