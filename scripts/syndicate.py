#!/usr/bin/env python3
"""POSSE syndication: push newly-published micro notes to the socials.

Reads the LIVE feed (so it only ever posts notes already visible on the site —
backlinks are never dead), tracks what's been posted in data/syndicated.json
(idempotent), posts to each enabled platform, and writes the returned post URLs
back into the note's `syndication:` front matter.

Each platform is independent: missing credentials -> skipped, an error on one ->
logged and the others still run. X is additionally gated behind X_ENABLED.

Env (all optional; a platform is skipped if its vars are absent):
  BLUESKY_HANDLE, BLUESKY_APP_PASSWORD
  MASTODON_INSTANCE, MASTODON_TOKEN
  NOSTR_NSEC
  THREADS_TOKEN, THREADS_USER_ID
  X_ENABLED (true/false), X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
  SUBSTACK_SID (+ optional SUBSTACK_LLI, SUBSTACK_CSRF, SUBSTACK_HANDLE, SUBSTACK_NOTES_BASE)
  SITE_BASE (default https://rishikeshs.com)

Substack has no official API: the Substack poster drives the same private
/api/v1 endpoints the web app uses (POST /api/v1/comment/feed with a ProseMirror
bodyJson — endpoint confirmed across community clients), authenticated by your
session cookies (pattern reused from the substack-api repo). A PREFLIGHT check
runs first and flags-and-skips on failure instead of posting blind.

KNOWN LIMITATION: these endpoints sit behind Cloudflare Bot Management, which
403s requests from datacenter IPs (GitHub Actions, Cloudflare Workers, Render,
Fly, Vercel) regardless of a valid cookie — only residential IPs pass, and TLS
fingerprint spoofing (curl_cffi) does NOT bypass the JS challenge. So Substack
syndication from this hourly Action will almost certainly 403 and be skipped;
to actually auto-post, run this step from a residential connection (a home
machine / cron), or keep Substack manual.
"""
import os
import json
import sys

import requests
import frontmatter

SITE = os.environ.get("SITE_BASE", "https://rishikeshs.com").rstrip("/")
FEED = f"{SITE}/micro/index.json"
STATE_PATH = os.path.join("data", "syndicated.json")
HTTP_TIMEOUT = 25


# --------------------------------------------------------------- state / io

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    os.makedirs("data", exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def fetch_feed():
    try:
        r = requests.get(FEED, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json().get("items", [])
    except Exception as e:
        print(f"Could not fetch feed {FEED}: {e}")
        return []


def download(url):
    r = requests.get(url, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.content


def text_of(item):
    """Syndicated text = the note body, with its optional link appended so
    followers on the silos can click through (the blog shows the link
    separately via the `link` front matter)."""
    t = (item.get("content_text") or "").strip()
    link = (item.get("link") or "").strip()
    if link and link not in t:
        t = (t + "\n\n" + link).strip()
    return t


# ----------------------------------------------------------------- posters
# Each returns a post URL on success, or None if not configured.

def post_bluesky(item):
    handle = os.environ.get("BLUESKY_HANDLE")
    pw = os.environ.get("BLUESKY_APP_PASSWORD")
    if not (handle and pw):
        return None
    from atproto import Client
    client = Client()
    client.login(handle, pw)
    img = item.get("image")
    if img:
        resp = client.send_image(text=text_of(item), image=download(img), image_alt=item.get("title") or "")
    else:
        resp = client.send_post(text=text_of(item))
    rkey = resp.uri.split("/")[-1]
    return f"https://bsky.app/profile/{handle}/post/{rkey}"


def post_mastodon(item):
    base = os.environ.get("MASTODON_INSTANCE")
    token = os.environ.get("MASTODON_TOKEN")
    if not (base and token):
        return None
    from mastodon import Mastodon
    m = Mastodon(access_token=token, api_base_url=base)
    media_ids = None
    img = item.get("image")
    if img:
        md = m.media_post(download(img), mime_type="image/webp")
        media_ids = [md["id"]]
    status = m.status_post(text_of(item), media_ids=media_ids)
    return status["url"]


def post_nostr(item):
    nsec = os.environ.get("NOSTR_NSEC")
    if not nsec:
        return None
    import time
    from pynostr.event import Event
    from pynostr.key import PrivateKey
    from pynostr.relay_manager import RelayManager

    pk = PrivateKey.from_nsec(nsec) if nsec.startswith("nsec") else PrivateKey(bytes.fromhex(nsec))
    content = text_of(item)
    img = item.get("image")
    if img:
        content = (content + "\n\n" + img).strip()
    ev = Event(content=content, pubkey=pk.public_key.hex())
    ev.sign(pk.hex())
    rm = RelayManager(timeout=6)
    for relay in ("wss://relay.damus.io", "wss://nos.lol", "wss://relay.nostr.band"):
        rm.add_relay(relay)
    rm.publish_event(ev)
    rm.run_sync()
    time.sleep(2)
    rm.close_all_relay_connections()
    return f"https://njump.me/{ev.id}"


def post_threads(item):
    token = os.environ.get("THREADS_TOKEN")
    uid = os.environ.get("THREADS_USER_ID")
    if not (token and uid):
        return None
    base = "https://graph.threads.net/v1.0"
    params = {"access_token": token, "text": text_of(item)}
    img = item.get("image")
    params["media_type"] = "IMAGE" if img else "TEXT"
    if img:
        params["image_url"] = img
    c = requests.post(f"{base}/{uid}/threads", data=params, timeout=HTTP_TIMEOUT).json()
    cid = c.get("id")
    if not cid:
        raise RuntimeError(f"threads container failed: {c}")
    pub = requests.post(f"{base}/{uid}/threads_publish",
                        data={"creation_id": cid, "access_token": token}, timeout=HTTP_TIMEOUT).json()
    pid = pub.get("id")
    if not pid:
        raise RuntimeError(f"threads publish failed: {pub}")
    perm = requests.get(f"{base}/{pid}", params={"fields": "permalink", "access_token": token},
                        timeout=HTTP_TIMEOUT).json()
    return perm.get("permalink", f"https://www.threads.net/@me/post/{pid}")


def post_x(item):
    if os.environ.get("X_ENABLED", "").lower() not in ("1", "true", "yes"):
        return None
    ck = os.environ.get("X_API_KEY")
    cs = os.environ.get("X_API_SECRET")
    at = os.environ.get("X_ACCESS_TOKEN")
    ats = os.environ.get("X_ACCESS_SECRET")
    if not all([ck, cs, at, ats]):
        return None
    import tempfile
    import tweepy
    media_ids = None
    img = item.get("image")
    if img:
        api = tweepy.API(tweepy.OAuth1UserHandler(ck, cs, at, ats))
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as f:
            f.write(download(img))
            fn = f.name
        media_ids = [api.media_upload(fn).media_id]
    client = tweepy.Client(consumer_key=ck, consumer_secret=cs,
                           access_token=at, access_token_secret=ats)
    resp = client.create_tweet(text=text_of(item), media_ids=media_ids)
    return f"https://x.com/i/web/status/{resp.data['id']}"


def _substack_session(base):
    """Build a requests session from the Substack cookies (same pattern as the
    substack-api repo: substack.sid + optional lli + csrf)."""
    sid = os.environ.get("SUBSTACK_SID")
    if not sid:
        return None
    host = base.split("//", 1)[-1].split("/", 1)[0]
    s = requests.Session()
    s.cookies.set("substack.sid", sid, domain="." + host, path="/")
    lli = os.environ.get("SUBSTACK_LLI")
    if lli:
        s.cookies.set("substack.lli", lli, domain="." + host, path="/")
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": base,
        "Referer": f"{base}/notes",
    })
    csrf = os.environ.get("SUBSTACK_CSRF")
    if csrf:
        s.headers["x-csrf-token"] = csrf
    return s


def substack_preflight(s, base):
    """Confirm the session is logged in AND that this IP isn't being Cloudflare-
    blocked, before we try to post. /api/v1/user/profile/self is the verified
    cookie-validation endpoint (returns your profile + owned publications).
    Raises so the caller flags-and-skips; returns True when good."""
    try:
        r = s.get(f"{base}/api/v1/user/profile/self", timeout=HTTP_TIMEOUT)
    except Exception as e:
        raise RuntimeError(f"preflight could not reach Substack: {e}")
    if r.status_code == 403:
        raise RuntimeError(
            "403 — Cloudflare is bot-blocking this IP, NOT a bad cookie. "
            "Substack's private endpoints reject datacenter IPs (GitHub Actions, "
            "Cloudflare Workers, Render, Fly, Vercel all fail); only residential "
            "IPs pass. Run the Substack step from a home connection or skip it.")
    if r.status_code == 401:
        raise RuntimeError("401 — session expired/invalid; refresh SUBSTACK_SID")
    if r.status_code >= 400:
        raise RuntimeError(f"preflight unexpected status {r.status_code} — endpoint may have changed")
    return True


def post_substack(item):
    base = os.environ.get("SUBSTACK_NOTES_BASE", "https://substack.com").rstrip("/")
    s = _substack_session(base)
    if s is None:
        return None
    text = text_of(item)
    if not text:
        return None  # notes are text-first; nothing to say -> skip
    substack_preflight(s, base)  # raises -> flagged & skipped by main loop
    body = {
        "bodyJson": {
            "type": "doc",
            "attrs": {"schemaVersion": "v1"},
            "content": [{"type": "paragraph",
                         "content": [{"type": "text", "text": text}]}],
        },
        "tabId": "for-you",
        "surface": "feed",
        "replyMinimumRole": "everyone",
    }
    r = s.post(f"{base}/api/v1/comment/feed", json=body, timeout=HTTP_TIMEOUT)
    if r.status_code == 403:
        raise RuntimeError("403 on post — Cloudflare blocked this IP (see preflight note)")
    r.raise_for_status()
    data = r.json()
    nid = data.get("id")
    if not nid:
        raise RuntimeError(f"note posted but no id in response: {data}")
    handle = os.environ.get("SUBSTACK_HANDLE")
    return (f"https://substack.com/@{handle}/note/c-{nid}" if handle
            else f"https://substack.com/note/c-{nid}")


PLATFORMS = [
    ("bluesky", post_bluesky),
    ("mastodon", post_mastodon),
    ("nostr", post_nostr),
    ("threads", post_threads),
    ("substack", post_substack),
    ("x", post_x),
]


# ----------------------------------------------------------- front matter

def update_frontmatter(item, entry):
    rel = item.get("_path")
    if not rel:
        return
    path = os.path.join("content", rel)
    if not os.path.exists(path):
        print(f"  content file missing, cannot write backlinks: {path}")
        return
    post = frontmatter.load(path)
    # Preserve manual backlinks (e.g. X / Substack posted by hand via the CMS):
    # keep any existing syndication entry whose platform isn't managed by the
    # auto-syndication state, then add/refresh the auto-posted ones.
    auto = set(entry.keys())
    existing = post.get("syndication") or []
    kept = [e for e in existing
            if isinstance(e, dict) and e.get("platform") not in auto]
    post["syndication"] = kept + [{"platform": p, "url": u} for p, u in entry.items()]
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
        f.write("\n")


# ------------------------------------------------------------------- main

def main():
    items = fetch_feed()
    if not items:
        print("No feed items — nothing to syndicate.")
        return
    state = load_state()
    changed = False

    for item in items:
        iid = item.get("id")
        if not iid:
            continue
        entry = dict(state.get(iid, {}))
        # Per-post targets chosen in the CMS; empty/absent -> all configured platforms.
        targets = item.get("syndicate_to") or None
        posted_here = False
        for name, fn in PLATFORMS:
            if targets is not None and name not in targets:
                continue
            if name in entry:
                continue
            try:
                url = fn(item)
            except Exception as e:
                print(f"[{name}] error for {iid}: {e}")
                continue
            if url:
                entry[name] = url
                posted_here = True
                changed = True
                print(f"[{name}] posted {iid} -> {url}")
        if entry:
            state[iid] = entry
            if posted_here:
                update_frontmatter(item, entry)

    if changed:
        save_state(state)
        print("state updated")
    else:
        print("no new syndications")


if __name__ == "__main__":
    sys.exit(main())
