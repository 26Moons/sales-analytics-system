import os
import glob
import pandas as pd
from etl_scripts.utils import get_logger
from etl_scripts.config_loader import load_config
from etl_scripts.archive_manager import move_to_archive,handle_file

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "sales_data", "raw")
PROCESSED = os.path.join(ROOT, "sales_data", "processed")
ARCHIVE = os.path.join(ROOT, "sales_data", "archive")

logger = get_logger("log")
configs = load_config()

def get_latest_file(folder_path : str , extension : str = "*.csv" ):
    # got the folder of new files from configs instance
    # rturns the latest file path
    files = glob.glob(os.path.normpath(os.path.join(folder_path,extension)))
    if not files:
        logger.error(f'No new files are there in {folder_path}')
        return None
    new_file = max(files , key = os.path.getctime)
    logger.info(f'New file found {new_file}')
    return new_file


    

def extract_data(file_path):
    # it doesnt need , however recievables from imports can be given
    # returns a dataframe
    try:
        raw_folder = configs["paths"]["raw_data"]
        og_schema = configs["schema"]["columns"]
        file_path = get_latest_file(raw_folder)

        if not file_path:
            return None
        
        status = handle_file(file_path, PROCESSED, ARCHIVE, use_checksum=False)
        if status == "new":
            # simulate ETL steps

            df = pd.read_csv(file_path)

            missing_cols = [col for col in og_schema if col not in df.columns]
            
            df = df[[c for c in df.columns if c in og_schema]]

            if (len(missing_cols)) != 0:
                logger.info(f"{len(missing_cols)} columns are missing")
                for col in missing_cols:
                    df[col] = None

            archived = move_to_archive(fp, ARCHIVE)
            logger.info("After processing moved original to archive: %s", archived)
            return df

        else:
            logger.info("File status: %s (no processing performed)", status)
            return none


    except Exception as e:
        logger.info("error is %s",e)
        return None