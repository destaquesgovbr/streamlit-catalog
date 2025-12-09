#!/usr/bin/env python3
"""
Fetch metadata from all DGB Streamlit application repositories.

This script queries the GitHub API to find all Streamlit app repositories
in the destaquesgovbr organization and extracts their metadata from the
.streamlit-app.yaml file.
"""

import json
import os
import sys
from typing import Dict, List
import yaml
import requests


GITHUB_ORG = "destaquesgovbr"
GITHUB_API_BASE = "https://api.github.com"
OUTPUT_FILE = "data/apps.json"


def get_github_token() -> str:
    """Get GitHub token from environment."""
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GH_TOKEN or GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    return token


def fetch_streamlit_repos(token: str) -> List[Dict]:
    """Fetch all repositories in the organization that are Streamlit apps."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get all repos in the organization
    repos_url = f"{GITHUB_API_BASE}/orgs/{GITHUB_ORG}/repos"
    params = {"per_page": 100, "type": "public"}

    repos = []
    page = 1

    while True:
        params["page"] = page
        response = requests.get(repos_url, headers=headers, params=params)
        response.raise_for_status()

        page_repos = response.json()
        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    # Filter for Streamlit apps (repos starting with "streamlit-" but not the boilerplate or catalog)
    streamlit_repos = [
        repo for repo in repos
        if repo["name"].startswith("streamlit-")
        and repo["name"] not in ["streamlit-boilerplate", "streamlit-catalog"]
    ]

    print(f"Found {len(streamlit_repos)} Streamlit app repositories")
    return streamlit_repos


def fetch_app_metadata(repo: Dict, token: str) -> Dict | None:
    """Fetch .streamlit-app.yaml metadata from a repository."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    repo_name = repo["name"]

    # Try to fetch .streamlit-app.yaml
    content_url = f"{GITHUB_API_BASE}/repos/{GITHUB_ORG}/{repo_name}/contents/.streamlit-app.yaml"

    try:
        response = requests.get(content_url, headers=headers)
        response.raise_for_status()

        # Decode base64 content
        import base64
        content_data = response.json()
        yaml_content = base64.b64decode(content_data["content"]).decode("utf-8")

        # Parse YAML
        metadata = yaml.safe_load(yaml_content)

        # Add repository information
        metadata["_repo_name"] = repo_name
        metadata["_repo_url"] = repo["html_url"]
        metadata["_last_updated"] = repo["updated_at"]
        metadata["_stars"] = repo["stargazers_count"]

        print(f"  ✓ {repo_name}: {metadata.get('name', 'Unknown')}")
        return metadata

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"  ✗ {repo_name}: .streamlit-app.yaml not found")
        else:
            print(f"  ✗ {repo_name}: HTTP error {e.response.status_code}")
        return None
    except Exception as e:
        print(f"  ✗ {repo_name}: Error - {e}")
        return None


def main():
    """Main function to fetch all app metadata."""
    print("Fetching Streamlit app metadata from GitHub...\n")

    token = get_github_token()

    # Fetch all Streamlit repos
    repos = fetch_streamlit_repos(token)

    # Fetch metadata for each repo
    print("\nFetching metadata files:")
    apps = []
    for repo in repos:
        metadata = fetch_app_metadata(repo, token)
        if metadata:
            apps.append(metadata)

    # Save to JSON file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(apps, f, indent=2)

    print(f"\n✓ Saved metadata for {len(apps)} apps to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
