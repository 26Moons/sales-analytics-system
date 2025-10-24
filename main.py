from etl_scripts.config_loader import load_config
from etl_scripts.extract import extract_data
from etl_scripts.transform import transform
from etl_scripts.load import load_to_postgres
from etl_scripts.utils import get_logger

def main():

    try:
        logger = get_logger("ETL")
        logger.info("ETL started")

        df = extract_data()
        logger.info("data extraction done")

        df_transformed = transform(df)
        logger.info("data transformation done")

        load_to_postgres(df_transformed)

        logger.info("ETL completed ")
    except Exception as e:
        logger.info("error happened %s",e)

if __name__ == "__main__":
    main()