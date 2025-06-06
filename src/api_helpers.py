import logging
from src.constants import OWNER, REPO
from src.github_api_client import GitHubAPIClient

logger = logging.getLogger(__name__)

def check_code_review_passed(pr_number: int) -> bool:
    """
    Checks if a specific pull request has at least one 'APPROVED' review.

    Args:
        pr_number (int): The number of the pull request to check.

    Returns:
        bool: True if the PR was approved, False otherwise.

    Raises:
        ValueError: When unexpected API-related errors occur.
    """
    try:
        api_client = GitHubAPIClient()
        response = api_client.get_pull_request_reviews(OWNER, REPO, pr_number)
        reviews = response.json()
        
        for review in reviews:
            if review['state'] == 'APPROVED':
                logger.info(f"PR #{pr_number} has at least one 'APPROVED' review.")
                return True
            
        logger.debug(f"PR #{pr_number} has no 'APPROVED' review.")
        return False
        
    except ValueError as e:
        if "GitHub PAT not found" in str(e):
            logger.error("GitHub PAT not found in api_helpers. Disabling API checks.")
            return False
        raise
    except Exception as e:
        logger.error(f"Error fetching reviews for PR #{pr_number}: {e}")
        return False

def check_all_checks_passed(commit_sha: str) -> bool:
    """
    Checks the combined status of a specific commit.

    Args:
        commit_sha (str): The SHA of the commit to check.

    Returns:
        bool: True if the combined status is 'success', False otherwise.

    Raises:
        ValueError: When unexpected API-related errors occur.
    """
    try:
        api_client = GitHubAPIClient()
        response = api_client.get_commit_status(OWNER, REPO, commit_sha)
        status = response.json()
        
        if status['state'] == 'success':
            logger.debug(f"Commit {commit_sha[:7]} has 'success' status.")
            return True
        else:
            logger.debug(f"Commit {commit_sha[:7]} has status {status['state']}.")
            return False
        
    except ValueError as e:
        if "GitHub PAT not found" in str(e):
            logger.error("GitHub PAT not found in api_helpers. Disabling API checks.")
            return False
        raise
    except Exception as e:
        logger.error(f"Error fetching status for commit {commit_sha[:7]}: {e}")
        return False