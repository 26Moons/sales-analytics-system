import os
from etl_scripts.config_loader import load_config
from etl_scripts.extract import extract_data, get_latest_file
from etl_scripts.transform import transform
from etl_scripts.archive_manager import handle_file 
from etl_scripts.load import load_to_postgres
from etl_scripts.utils import get_logger

config = load_config()
logger = get_logger("ETL_Main")



status = handle_file(file_path, PROCESSED, ARCHIVE, use_checksum=False)


def main():

    try:
        logger.info("🚀 Starting ETL pipeline")

        raw_dir = config["paths"]["raw"]
        processed_dir = config["paths"]["processed"]
        archive_dir = config["paths"]["archive"]

        # STEP 1 — Extract
        file_path = get_latest_file(raw_dir)
        if not file_path:
            logger.warning("⚠️ No new file found to process")
            return "no_file"

        logger.info("data extraction done")


        # STEP 2 - Archive check
        file_status = handle_file(file_path, processed_dir, archive_dir)
        if file_status == "archived":
            logger.info(f"File {file_path} already processed, skipping.")
            return "already_archived"

        # STEP 3 - Transform Data
        df_transformed = transform(df)
        logger.info("data transformation done")

        # STEP 4 - Load Data
        load_to_postgres(df_transformed)

        logger.info("ETL completed ")
        return "success"
    except Exception as e:
        logger.info("error happened %s",e)
        return "error"

if __name__ == "__main__":
    main()