import os
import glob
import pandas as pd
from etl_scripts.utils import get_logger
from etl_scripts.config_loader import load_config

logger = get_logger("log")
configs = load_config()

def get_latest_file(folder_path : str , extension : str = "*.csv" ):
    # got the folder of new files from configs instance
    # rturns the latest file path
    files = glob.glob(os.path.join(folder,extension))
    if not files:
        logger.error(f'No new files are there in {folder}')
        return None
    new_file = max(files , key=os.path.getctime)
    logger.info(f'New file found {new_file}')



def extract_data():
    # it doesnt need , however recievables from imports can be given
    # returns a dataframe
    try:
        raw_folder = configs["paths"]["raw_data"]
        og_schema = configs["schema"]["columns"]

        file_path = get_latest_file(raw_folder)
        if not file_path:
            return None
        
        df = pd.read_csv(file_path)

        missing_cols = [col for col in og_schema if col not in df.columns]
        
        for col in missing_cols:
            df[col] = 'None'

        return df
    except Exception as e:
        logger.info("error is %s",e)
        return None