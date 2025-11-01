import os
from etl_scripts.config_loader import load_config
from etl_scripts.extract import extract_data, get_latest_file
from etl_scripts.transform import transform
from etl_scripts.archive_manager import handle_file,move_to_archive 
from etl_scripts.load import load_to_postgres
from etl_scripts.utils import get_logger

config = load_config()
logger = get_logger("ETL_Main")



ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
logger.info(f"Root directory resolved at: {ROOT}")
RAW = os.path.join(ROOT, "sales_data", "raw")
PROCESSED = os.path.join(ROOT, "sales_data", "processed")
ARCHIVE = os.path.join(ROOT, "sales_data", "archive")





def main():

    try:
        logger.info("🚀 Starting ETL pipeline")



        # STEP 1 — Fetch latest file
        file_path = get_latest_file(RAW)
        logger.info("latest file fetched %s", file_path)
        if not file_path:
            logger.warning("⚠️ No new valid csv file found to process")
            return "no_file"
        # STEP 2 - Archive check
        status = handle_file(file_path, PROCESSED, ARCHIVE, use_checksum=False)
        # STEP 3 - Extract Data
        df = extract_data(status, file_path)
        logger.info("data extraction done")


        # STEP 3 - Transform Data
        df_transformed = transform(df)
        logger.info("data transformation done")

        # STEP 4 - Load Data
        load_to_postgres(df_transformed)

        # STEP 5 - Move the processed file to archive
        archived = move_to_archive(file_path, ARCHIVE)
        logger.info("After processing moved original to archive: %s", archived)

        logger.info("ETL completed ")
        return "success"
    except Exception as e:
        logger.info("error happened %s",e)
        return "error"

if __name__ == "__main__":
    main()