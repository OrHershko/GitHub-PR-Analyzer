from src.extract import fetch_pull_requests
from src.logging_config import setup_logging
import logging
from src.constants import RAW_PULL_REQUESTS_PATH, PROCESSED_REPORT_PATH
from src.transform import process_pull_requests
import argparse

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # -- Parse command line arguments --
    parser = argparse.ArgumentParser(description="Fetch and analyze GitHub PRs for compliance.")
    parser.add_argument(
        "--start-date",
        type=str,
        help="Filter PRs merged on or after this date. Format: YYYY-MM-DD"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="Filter PRs merged on or before this date. Format: YYYY-MM-DD"
    )
    args = parser.parse_args()

    # -- Start GitHub PR Analysis --
    logger.info("--- Starting GitHub PR Analysis ---")
    if args.start_date or args.end_date:
        logger.info(f"Running with date filter: Start: {args.start_date}, End: {args.end_date}")

    logger.info(">>> Step 1: Extracting data from GitHub...")
    try:
        fetch_pull_requests(output_path=RAW_PULL_REQUESTS_PATH)
    except Exception as e:
        logger.exception(f"An error occurred during data extraction: {e}")
        return

    logger.info("Extraction step completed successfully.")
    logger.info(">>> Step 2: Processing data...")

    try:
        process_pull_requests(
            input_path=RAW_PULL_REQUESTS_PATH,
            output_path=PROCESSED_REPORT_PATH,
            start_date=args.start_date if args.start_date else None,
            end_date=args.end_date if args.end_date else None
        )
    except Exception as e:
        logger.exception(f"An error occurred during data transformation: {e}")
        return

    logger.info("Transformation step completed successfully.")

    logger.info("--- GitHub PR Analysis Finished ---")


if __name__ == "__main__":
    main()



