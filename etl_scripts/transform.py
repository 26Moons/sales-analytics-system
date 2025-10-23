import pandas as pd
from etl_scripts.utils import get_logger

logger = get_logger("etl")

def transform(df : pd.DataFrame):
    try:
        if df is None or df.empty:
            logger.warning("No data recieved for transformation")
            return df

        df = df.drop_duplicates()
        df.columns = [col.strip() for col in df.columns]
        df['total_sales'] = df['quantity'] * df['unit_price']
        df['order_date'] = pd.to_datetime(df['order_date'])

        logger.info(f"Data transformed , shape is {df.shape}")

        return df    

    except Exception as e:
        logger.info("error is %s",e)
        return None