import json
import logging
import time
import pandas as pd
from pathlib import Path

from src.api_helpers import check_all_checks_passed, check_code_review_passed

logger = logging.getLogger(__name__)

def process_pull_requests(input_path: Path, output_path: Path, start_date: str = None, end_date: str = None):
    """
    Reads raw pull request data, optionally filters it by date, enriches it,
    and saves the final report.

    Args:
        input_path (Path): Path to the raw JSON file of pull requests.
        output_path (Path): Path to save the final CSV report.
        start_date (str): Optional start date for filtering PRs.
        end_date (str): Optional end date for filtering PRs.
    """
    logger.info(f"Reading raw data from {input_path}...")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_prs = json.load(f)
    except FileNotFoundError:
        logger.error(f"Input file not found at {input_path}. Please run the extraction step first.")
        return
    
    if not raw_prs:
        logger.warning("Input file is empty. No data to process.")
        return
    
    df = pd.DataFrame(raw_prs)
    logger.info(f"Loaded {len(df)} total merged PRs.")

    if start_date or end_date:
        logger.info("Applying date filter...")
        df = filter_by_date(df, start_date, end_date)
        logger.info(f"Found {len(df)} PRs within the specified date range.")
    
    if df.empty:
        logger.warning("No pull requests match the specified date range. Nothing to process.")
        return

    processed_prs = []
    for i, pr in df.iterrows():
        pr_number = pr['number']
        commit_sha = pr['head']['sha']
        
        logger.info(f"Processing PR #{pr_number} ({i+1}/{len(df)})...")
        cr_passed = check_code_review_passed(pr_number)
        checks_passed = check_all_checks_passed(commit_sha)

        processed_prs.append({
            "pr_number": pr_number,
            "pr_title": pr['title'],
            "author": pr['user']['login'],
            "merge_date": pr['merged_at'],
            "CR_Passed": cr_passed,
            "CHECK_PASSED": checks_passed,
        })

        # Small delay to avoid rate limiting
        time.sleep(0.1)


    df = pd.DataFrame(processed_prs)

    if not df.empty:
        # Format merge_date to YYYY-MM-DD HH:MM:SS
        df['merge_date'] = pd.to_datetime(df['merge_date']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    logger.info(f"Successfully processed {len(df)} pull requests. Report saved to {output_path}")


    
def filter_by_date(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Filters a DataFrame of PRs by merge date.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        start_date (str): The start date for filtering.
        end_date (str): The end date for filtering.
    """
    if start_date:
        df = df[df['merged_at'] >= start_date]
    if end_date:
        df = df[df['merged_at'] <= end_date]
    return df