#!/usr/bin/env python3
"""
Fetch all unique contributors from barosl/homu, rust-lang/homu, and rust-lang/bors
repositories. Download their GitHub usernames and avatar images.
"""

import json
import os
import tempfile
import time
from pathlib import Path

import git
import requests

REPOS = [
    ("graydon/bors", "https://github.com/graydon/bors.git"),
    ("servo/homu", "https://github.com/servo/homu.git"),
    ("barosl/homu", "https://github.com/barosl/homu.git"),
    ("rust-lang/homu", "https://github.com/rust-lang/homu.git"),
    ("rust-lang/bors", "https://github.com/rust-lang/bors.git"),
]

OUTPUT_DIR = Path(__file__).parent / "contributors"
AVATARS_DIR = OUTPUT_DIR / "avatars"
USERNAMES_FILE = OUTPUT_DIR / "usernames.json"

GITHUB_API = "https://api.github.com"
RUST_TEAM_API = "https://team-api.infra.rust-lang.org/v1/people.json"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def get_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers


def fetch_rust_team_people() -> dict:
    """Fetch the Rust team people database. Returns {email -> {login, github_id}} and {name_lower -> {login, github_id}}."""
    print("Fetching Rust team API data...")
    resp = requests.get(RUST_TEAM_API, timeout=30)
    resp.raise_for_status()
    people = resp.json().get("people", {})

    by_email = {}
    by_name = {}
    for github_login, info in people.items():
        entry = {"login": github_login, "github_id": info.get("github_id")}
        email = info.get("email")
        if email:
            by_email[email.lower()] = entry
        name = info.get("name")
        if name:
            by_name[name.lower()] = entry

    print(f"  Loaded {len(people)} people ({len(by_email)} with emails)")
    return by_email, by_name


def fetch_github_contributors(owner_repo: str) -> dict:
    """Fetch contributors for a repo using the GitHub API. Returns {login -> avatar_url}."""
    contributors = {}
    page = 1
    while True:
        resp = requests.get(
            f"{GITHUB_API}/repos/{owner_repo}/contributors",
            params={"per_page": 100, "page": page, "anon": 0},
            headers=get_headers(),
        )
        if resp.status_code != 200:
            print(f"  Warning: GitHub API returned {resp.status_code} for {owner_repo} contributors")
            break
        data = resp.json()
        if not data:
            break
        for item in data:
            if item.get("type") == "User":
                contributors[item["login"]] = item["avatar_url"]
        page += 1
    return contributors


def collect_commit_emails_and_names(repo_url: str, tmpdir: str, label: str) -> set[tuple[str, str]]:
    """Clone a repo and collect all unique (name, email) pairs from commits."""
    print(f"Cloning {label}...")
    repo_path = os.path.join(tmpdir, label.replace("/", "_"))
    repo = git.Repo.clone_from(repo_url, repo_path)

    contributors = set()
    for commit in repo.iter_commits("--all"):
        contributors.add((commit.author.name, commit.author.email))
        contributors.add((commit.committer.name, commit.committer.email))

    print(f"  Found {len(contributors)} unique (name, email) pairs in {label}")
    return contributors


def github_api_with_retry(url, params=None, headers=None, max_retries=3):
    """Make a GitHub API request with rate limit handling."""
    for attempt in range(max_retries):
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_time = int(resp.headers.get("X-RateLimit-Reset", 0))
            wait = max(reset_time - int(time.time()), 5)
            print(f"  Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        return resp
    return resp


def resolve_github_username(email: str, name: str) -> dict | None:
    """Try to resolve a GitHub username from a commit email via the GitHub API."""
    # Handle GitHub noreply emails
    if email.endswith("@users.noreply.github.com"):
        username = email.split("@")[0]
        # Handle numeric prefix format: 12345+username or username+12345
        if "+" in username:
            parts = username.split("+")
            for p in parts:
                if not p.isdigit():
                    username = p
                    break
        return lookup_user(username)

    # Search commits by email
    resp = github_api_with_retry(
        f"{GITHUB_API}/search/commits",
        params={"q": f"author-email:{email}", "per_page": 1},
        headers={**get_headers(), "Accept": "application/vnd.github.cloak-preview+json"},
    )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("total_count", 0) > 0:
            author = data["items"][0].get("author")
            if author:
                return {"login": author["login"], "avatar_url": author["avatar_url"]}

    # Fallback: search users by email
    resp = github_api_with_retry(
        f"{GITHUB_API}/search/users",
        params={"q": f"{email} in:email", "per_page": 1},
        headers=get_headers(),
    )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("total_count", 0) > 0:
            item = data["items"][0]
            return {"login": item["login"], "avatar_url": item["avatar_url"]}

    return None


def lookup_user(username: str) -> dict | None:
    """Look up a GitHub user by username."""
    resp = requests.get(f"{GITHUB_API}/users/{username}", headers=get_headers(), timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        return {"login": data["login"], "avatar_url": data["avatar_url"]}
    return None


def resolve_from_rust_team(email: str, name: str, by_email: dict, by_name: dict) -> str | None:
    """Try to resolve a GitHub username from the Rust team API data."""
    print(f"Resolving {email}/{name} from team")
    # Try email match first
    result = by_email.get(email.lower())
    if result:
        print(f"Found login {result}")
        return result["login"]

    # Try name match
    result = by_name.get(name.lower())
    if result:
        print(f"Found login {result}")
        return result["login"]

    return None


def download_avatar(login: str, avatar_url: str, output_dir: Path):
    """Download avatar image as PNG."""
    filepath = output_dir / f"{login}.png"
    if filepath.exists():
        print(f"  Avatar for {login} already exists, skipping")
        return
    url = avatar_url + ("&" if "?" in avatar_url else "?") + "s=256"
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        filepath.write_bytes(resp.content)
        print(f"  Saved avatar for {login}")
    else:
        print(f"  Failed to download avatar for {login}: {resp.status_code}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AVATARS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Fetch Rust team API data for fallback resolution
    rust_by_email, rust_by_name = fetch_rust_team_people()

    # Step 2: Fetch contributors via GitHub API (efficient, no rate limit issues)
    resolved = {}  # login -> avatar_url
    for label, _ in REPOS:
        print(f"Fetching GitHub contributors for {label}...")
        api_contributors = fetch_github_contributors(label)
        resolved.update(api_contributors)
        print(f"  Found {len(api_contributors)} contributors via API")

    print(f"\nTotal from GitHub API: {len(resolved)} unique contributors")

    # Step 3: Clone repos and collect commit emails to find any missed contributors
    all_contributors = set()
    with tempfile.TemporaryDirectory() as tmpdir:
        for label, url in REPOS:
            contributors = collect_commit_emails_and_names(url, tmpdir, label)
            all_contributors.update(contributors)

    print(f"\nTotal unique (name, email) pairs across all repos: {len(all_contributors)}")

    # Step 4: Try to resolve remaining contributors not found via the API
    seen_emails = set()
    unresolved = []

    for name, email in sorted(all_contributors):
        if email in seen_emails:
            continue
        seen_emails.add(email)

        # Skip known bot/noreply
        if email == "noreply@github.com":
            continue
        if "[bot]" in email or "[bot]" in name:
            continue

        # Check if already resolved
        # For noreply emails, extract username and check
        if email.endswith("@users.noreply.github.com"):
            username = email.split("@")[0]
            if "+" in username:
                parts = username.split("+")
                for p in parts:
                    if not p.isdigit():
                        username = p
                        break
            if username.lower() in {k.lower() for k in resolved}:
                continue

        # Try Rust team API first (no rate limits)
        rust_login = resolve_from_rust_team(email, name, rust_by_email, rust_by_name)
        if rust_login:
            if rust_login not in resolved:
                print(f"Resolved {name} <{email}> -> {rust_login} (via Rust team API)")
                user_info = lookup_user(rust_login)
                if user_info:
                    resolved[user_info["login"]] = user_info["avatar_url"]
                else:
                    # Construct avatar URL from github_id if available
                    entry = rust_by_email.get(email.lower()) or rust_by_name.get(name.lower())
                    if entry and entry.get("github_id"):
                        resolved[rust_login] = f"https://avatars.githubusercontent.com/u/{entry['github_id']}"
            continue

        # Try GitHub API search
        print(f"Resolving {name} <{email}> via GitHub API...")
        result = resolve_github_username(email, name)
        if result:
            login = result["login"]
            if login not in resolved:
                resolved[login] = result["avatar_url"]
                print(f"  -> {login}")
            else:
                print(f"  -> {login} (already known)")
        else:
            unresolved.append((name, email))
            print(f"  -> Could not resolve")

    print(f"\nResolved {len(resolved)} unique GitHub users")
    if unresolved:
        print(f"Could not resolve {len(unresolved)} contributors:")
        for name, email in unresolved:
            print(f"  - {name} <{email}>")

    # Step 5: Save usernames to JSON
    usernames = sorted(resolved.keys(), key=str.lower)
    USERNAMES_FILE.write_text(json.dumps(usernames, indent=2) + "\n")
    print(f"\nSaved {len(usernames)} usernames to {USERNAMES_FILE}")

    # Step 6: Download avatars
    print("\nDownloading avatars...")
    for login in usernames:
        avatar_url = resolved[login]
        download_avatar(login, avatar_url, AVATARS_DIR)

    print(f"\nDone! {len(usernames)} contributors found.")


if __name__ == "__main__":
    main()