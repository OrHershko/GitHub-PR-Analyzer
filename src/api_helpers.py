import os
from dotenv import load_dotenv
import logging
import requests
from src.constants import GITHUB_API_URL, OWNER, REPO

logger = logging.getLogger(__name__)

load_dotenv()
PAT = os.getenv("GITHUB_PAT")

headers = {
    "Authorization": f"Bearer {PAT}",
    "Accept": "application/vnd.github.v3+json",
}

def check_code_review_passed(pr_number: int) -> bool:
    """
    Checks if a specific pull request has at least one 'APPROVED' review.

    Args:
        pr_number (int): The number of the pull request to check.

    Returns:
        bool: True if the PR was approved, False otherwise.
    """
    if not PAT:
        logger.error("GitHub PAT not found in api_helpers. Disabling API checks.")
        return False
    
    reviews_url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews"

    try:
        response = requests.get(reviews_url, headers=headers)
        response.raise_for_status()

        reviews = response.json()
        
        for review in reviews:
            if review['state'] == 'APPROVED':
                logger.info(f"PR #{pr_number} has at least one 'APPROVED' review.")
                return True
            
        logger.debug(f"PR #{pr_number} has no 'APPROVED' review.")
        return False
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching reviews for PR #{pr_number}: {e}")
        return False

def check_all_checks_passed(commit_sha: str) -> bool:
    """
    Checks the combined status of a specific commit.

    Args:
        commit_sha (str): The SHA of the commit to check.

    Returns:
        bool: True if the combined status is 'success', False otherwise.
    """
    if not PAT:
        logger.error("GitHub PAT not found in api_helpers. Disabling API checks.")
        return False
    
    status_url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/commits/{commit_sha}/status"
    
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        
        status = response.json()
        
        if status['state'] == 'success':
            logger.debug(f"Commit {commit_sha[:7]} has 'success' status.")
            return True
        else:
            logger.debug(f"Commit {commit_sha[:7]} has status {status['state']}.")
            return False
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching status for commit {commit_sha[:7]}: {e}")
        return False