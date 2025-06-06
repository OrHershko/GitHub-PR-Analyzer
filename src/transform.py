import json
import logging
import time
import pandas as pd
from pathlib import Path

from src.api_helpers import check_all_checks_passed, check_code_review_passed

logger = logging.getLogger(__name__)

def process_pull_requests(input_path: Path, output_path: Path):
    """
    Reads raw pull request data, processes it, and saves a structured report.
    In this initial version, it processes basic fields and uses placeholders
    for review and check statuses.

    Args:
        input_path (Path): Path to the raw JSON file of pull requests.
        output_path (Path): Path to save the final CSV report.
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
    
    logger.info(f"Starting to process {len(raw_prs)} pull requests...")

    processed_prs = []
    for i, pr in enumerate(raw_prs):
        pr_number = pr['number']
        commit_sha = pr['head']['sha']
        
        logger.info(f"Processing PR #{pr_number} ({i+1}/{len(raw_prs)})...")
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


    
