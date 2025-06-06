import logging
import json
import re
from pathlib import Path
from src.constants import OWNER, REPO
from src.github_api_client import GitHubAPIClient

logger = logging.getLogger(__name__)

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
    api_client = GitHubAPIClient()

    # The starting URL for the first page
    next_page_url = None
    params = {"state": "closed", "per_page": 100}

    all_closed_prs = []
    page_count = 1

    while True:
        logger.info(f"Fetching page {page_count} of closed PRs...")
        
        if next_page_url:
            # For subsequent pages, use the full URL from pagination
            response = api_client.make_request(next_page_url)
        else:
            # For the first page, use the helper method
            response = api_client.get_pull_requests(OWNER, REPO, **params)
        
        prs_on_page = response.json()
        
        if not prs_on_page:
            logger.info("Received an empty page, stopping.")
            break

        all_closed_prs.extend(prs_on_page)
        logger.info(f"Fetched {len(prs_on_page)} PRs on page {page_count}")

        page_count += 1
        next_page_url = parse_link_header(response.headers)
        
        # Break if no more pages
        if not next_page_url:
            break

    logger.info(f"Finished fetching. Total closed PRs found: {len(all_closed_prs)}")

    merged_prs = [pr for pr in all_closed_prs if pr.get("merged_at") is not None]

    logger.info(f"Found {len(merged_prs)} merged PRs in total after filtering.")

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_prs, f, ensure_ascii=False, indent=4)

    logger.info(f"Raw data successfully saved to {output_path}")







