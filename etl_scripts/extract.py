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
    logger.info(f"Resolved folder path: {os.path.abspath(folder_path)}")

    files = glob.glob(os.path.normpath(os.path.join(folder_path,extension)))
    logger.info(f'Looking for new files in {folder_path} with extension {extension} and {files} found')
    if not files:
        logger.error(f'No new files are there in {folder_path}')
        return None
    new_file = max(files , key = os.path.getctime)
    
    logger.info(f'New file found {new_file}')

    valid = is_valid_csv(new_file)
    if not valid:
        logger.error(f'File {new_file} is not a valid CSV format')
        return None
    return new_file


def is_valid_csv(file_path: str) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            header = f.readline()
            expected_cols = ["date", "region", "product", "sales", "quantity"]
            # Strip spaces and split
            cols = [col.strip().lower() for col in header.split(",")]
            if set(expected_cols).issubset(set(cols)):
                return True
            else:
                return False
    except Exception as e:
        logger.error(f"File validation failed for {file_path}: {e}")
        return False
    



def extract_data(status: str, file_path: str):
    # it doesnt need , however recievables from imports can be given
    # returns a dataframe
    try:
        
        if status == "new":


            df = pd.read_csv(file_path,sep= ",")
            logger.info(f"File {file_path} has {df.columns.tolist()} columns")

            logger.info(f"Data extracted , shape is {df.shape}")
            return df

        else:
            logger.info("File status: %s (no processing performed)", status)
            return None


    except Exception as e:
        logger.info("error is %s",e)
        return None