from pathlib import Path

"""
A central place for all project-wide constants.
"""

# --- GitHub API Configuration ---
GITHUB_API_URL = "https://api.github.com"
OWNER = "Scytale-exercise"
REPO = "scytale-repo3"

# --- File System Paths ---
# The root directory of the project
BASE_DIR = Path(__file__).parent.parent 

# Output directories
OUTPUT_DIR = BASE_DIR / "outputs"
RAW_DATA_DIR = OUTPUT_DIR / "raw"
PROCESSED_DATA_DIR = OUTPUT_DIR / "processed"
PROCESSED_REPORT_PATH = PROCESSED_DATA_DIR / "pr_report.csv"

# Output file paths
RAW_PULL_REQUESTS_PATH = RAW_DATA_DIR / "pull_requests.json"
