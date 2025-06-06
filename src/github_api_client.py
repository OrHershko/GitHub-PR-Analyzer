import os
import time
import logging
import requests
from dotenv import load_dotenv
from src.constants import GITHUB_API_URL

logger = logging.getLogger(__name__)

load_dotenv()

class GitHubAPIClient:
    """A GitHub API client with rate limiting, retries, and error handling."""
    
    def __init__(self):
        self.pat = os.getenv("GITHUB_PAT")
        if not self.pat:
            raise ValueError("GitHub PAT not found. Please ensure you have a .env file with GITHUB_PAT='your_token'")
        
        self.headers = {
            "Authorization": f"Bearer {self.pat}",
            "Accept": "application/vnd.github.v3+json",
        }
    
    def _handle_rate_limit(self, response: requests.Response) -> bool:
        """Handle GitHub API rate limiting with retry logic."""
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            logger.warning(f"Rate limit hit. Waiting {retry_after} seconds before retrying...")
            time.sleep(retry_after)
            return True
        return False
    
    def make_request(self, url: str, params: dict = None, max_retries: int = 3) -> requests.Response:
        """
        Make API request with retry logic and proper error handling.
        
        Args:
            url (str): The API endpoint URL
            params (dict, optional): Query parameters
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            requests.Response: The successful response object
            
        Raises:
            ValueError: When the response is not JSON
            requests.exceptions.RequestException: When all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                # Handle rate limiting
                if self._handle_rate_limit(response):
                    continue
                    
                response.raise_for_status()
                
                # Validate JSON response
                if not response.headers.get('content-type', '').startswith('application/json'):
                    logger.error(f"Expected JSON response, got {response.headers.get('content-type')}")
                    raise ValueError("Invalid response format")
                    
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout on attempt {attempt + 1}/{max_retries}")
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error on attempt {attempt + 1}/{max_retries}: {e}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed on attempt {attempt + 1}/{max_retries}: {e}")
                
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        raise requests.exceptions.RequestException(f"Failed to complete request after {max_retries} attempts")
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "closed", per_page: int = 100) -> requests.Response:
        """
        Get pull requests from a repository with pagination support.

        Args:
            owner (str): The owner of the repository
            repo (str): The name of the repository
            state (str): The state of the pull requests
            per_page (int): The number of pull requests per page
        """
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": per_page}
        return self.make_request(url, params)
    
    def get_pull_request_reviews(self, owner: str, repo: str, pr_number: int) -> requests.Response:
        """
        Get reviews for a specific pull request.

        Args:
            owner (str): The owner of the repository
            repo (str): The name of the repository
            pr_number (int): The number of the pull request
        """
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        return self.make_request(url)
    
    def get_commit_status(self, owner: str, repo: str, commit_sha: str) -> requests.Response:
        """
        Get the combined status for a specific commit.

        Args:
            owner (str): The owner of the repository
            repo (str): The name of the repository
            commit_sha (str): The SHA of the commit

        Returns:
            requests.Response: The successful response object
        """
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{commit_sha}/status"
        return self.make_request(url) 