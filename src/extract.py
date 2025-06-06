import os
from dotenv import load_dotenv
import requests
from src.constants import GITHUB_API_URL, OWNER, REPO
import logging
from pathlib import Path
import json
import re

logger = logging.getLogger(__name__)

load_dotenv()

PAT = os.getenv("GITHUB_PAT")

def parse_link_header(headers: dict) -> str | None:
    """
    Parses the Link header from a GitHub API response to find the 'next' page URL.

    Args:
        headers (dict): The response headers from the requests library.

    Returns:
        str | None: The URL for the next page, or None if it doesn't exist.
    """
    link_header = headers.get("Link")
    if not link_header:
        return None
  
    # The Link header format is: '<url1>; rel="next", <url2>; rel="last"'
    # We search for the part of the string that contains rel="next"
    links = link_header.split(',')

    for link in links:
        if 'rel="next"' in link:
            # Extract the URL from between the angle brackets <> using regex
            match = re.search(r'<(.*?)>', link)
            if match:
                return match.group(1)

    return None


def fetch_pull_requests(output_path: Path):
    """
    Fetches ALL closed pull requests from the GitHub repository using pagination.
    It then filters for PRs that were actually merged and saves the raw data.

    Args:
        output_path (Path): The path where the raw JSON file will be saved.
    """
    if not PAT:
        logger.error("GitHub Personal Access Token (PAT) not found. Please ensure you have a .env file with GITHUB_PAT='your_token'")
        raise ValueError("GitHub PAT not found.")

    headers = {
        "Authorization": f"Bearer {PAT}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    params = {
        "state": "closed",
        "per_page": 1,
    }

    # The starting URL for the first page
    next_page_url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls"

    all_closed_prs = []
    page_count = 1

    while next_page_url:
        logger.info(f"Fetching page {page_count} of closed PRs...")
        response = requests.get(next_page_url, headers=headers, params=params)
        response.raise_for_status()

        prs_on_page = response.json()
        if not prs_on_page:
            logger.info("Received an empty page, stopping.")
            break

        all_closed_prs.extend(prs_on_page)
        logger.info(f"Fetched {len(prs_on_page)} PRs on page {page_count}")

        # After the first request, the params are included in the next_page_url, so we don't need them.
        params = None 
        page_count += 1
        next_page_url = parse_link_header(response.headers)

    logger.info(f"\nFinished fetching. Total closed PRs found: {len(all_closed_prs)}")

    merged_prs = [pr for pr in all_closed_prs if pr.get("merged_at") is not None]

    logger.info(f"Found {len(merged_prs)} merged PRs in total after filtering.")

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_prs, f, ensure_ascii=False, indent=4)

    logger.info(f"Raw data successfully saved to {output_path}")







