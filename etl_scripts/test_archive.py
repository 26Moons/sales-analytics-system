# etl_scripts/test_archive.py
import os
import shutil
from etl_scripts.archive_manager import handle_file,move_to_archive
from etl_scripts.utils import get_logger

logger = get_logger("test_archive")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "sales_data", "raw")
PROCESSED = os.path.join(ROOT, "sales_data", "processed")
ARCHIVE = os.path.join(ROOT, "sales_data", "archive")

def simulate_processing(file_path):
    logger.info("%s",file_path)
    """Simulate actual processing by copying file to processed folder."""
    os.makedirs(PROCESSED, exist_ok=True) # exist_ok to make indempotent code
    dest = os.path.join(PROCESSED, os.path.basename(file_path))
    shutil.copy(file_path, dest)
    logger.info("Simulated processing, copied to processed: %s", dest)
    return dest

if __name__ == "__main__":
    # iterate all CSVs in raw and run the handler
    for fname in os.listdir(RAW):
        if not fname.lower().endswith(".csv"):
            continue
        fp = os.path.join(RAW, fname)
        status = handle_file(fp, PROCESSED, ARCHIVE, use_checksum=False)
        if status == "new":
            # simulate ETL steps
            processed_path = simulate_processing(fp)
            # after successful processing, move original raw file to archive
            archived = move_to_archive(fp, ARCHIVE)
            logger.info("After processing moved original to archive: %s", archived)
        else:
            logger.info("File status: %s (no processing performed)", status)

    logger.info("Test run complete.")
