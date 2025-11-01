import pandas as pd
from etl_scripts.utils import get_logger
from etl_scripts.config_loader import load_config
configs = load_config()
og_schema = configs["schema"]["columns"]
logger = get_logger("etl")

def transform(df : pd.DataFrame):
    try:
        if df is None or df.empty:
            logger.warning("No data recieved for transformation")
            return df

        df = df.drop_duplicates()
        df.columns = [col.strip() for col in df.columns]
        logger.info(f"Columns after stripping whitespaces: {df.columns.tolist()}")
        missing_cols = [col for col in og_schema if col not in df.columns]
        logger.info(f"Missing columns identified: {missing_cols}")
        df = df[[c for c in df.columns if c in og_schema]]
        logger.info(f"Columns after reordering: {df.columns.tolist()}")
        if (len(missing_cols)) != 0:
            logger.info(f"{len(missing_cols)} columns are missing")
            for col in missing_cols:
                df[col] = None

        

        logger.info(f"Data transformed , shape is {df.shape}")

        return df    

    except Exception as e:
        logger.info("error is %s",e)
        return None