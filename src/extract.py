import os
from dotenv import load_dotenv
import requests
from src.constants import GITHUB_API_URL, OWNER, REPO
import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)

load_dotenv()

PAT = os.getenv("GITHUB_PAT")

def fetch_pull_requests(output_path: Path):
    """
    Fetches the first page of closed pull requests from the GitHub repository,
    filters for merged ones, and saves the raw data to a JSON file.

    Args:
        output_path (Path): The path where the raw JSON file will be saved.
    """
    if not PAT:
        logger.error("GitHub Personal Access Token (PAT) not found. Please ensure you have a .env file with GITHUB_PAT='your_token'")
        raise ValueError("GitHub PAT not found.")

    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls"

    headers = {
        "Authorization": f"Bearer {PAT}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    params = {
        "state": "closed",
        "per_page": 100,
    }
    
    logger.info(f"Fetching data from: {url}")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() 

    all_closed_prs = response.json()

    merged_prs = [pr for pr in all_closed_prs if pr.get("merged_at") is not None]

    logger.info(f"Found {len(merged_prs)} merged PRs on the first page of results.")

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_prs, f, ensure_ascii=False, indent=4)

    logger.info(f"Raw data successfully saved to {output_path}")







