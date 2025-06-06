from src.extract import fetch_pull_requests
from src.logging_config import setup_logging
import logging
from src.constants import RAW_PULL_REQUESTS_PATH

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("--- Starting GitHub PR Analysis ---")


    logger.info(">>> Step 1: Extracting data from GitHub...")
    try:
        fetch_pull_requests(output_path=RAW_PULL_REQUESTS_PATH)
    except Exception as e:
        logger.exception(f"An error occurred during data extraction: {e}")
        return

    logger.info("Extraction step completed successfully.")
    logger.info("--- GitHub PR Analysis Finished ---")


if __name__ == "__main__":
    main()



