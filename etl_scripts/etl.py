import pandas as pd
from sqlalchemy import create_engine,text,Table
import logging

#------------------#
#  Logging Setup   #
#------------------#

logging.basicConfig(
    filename = 'logs/etl_logs.log',
    level = logging.INFO,
    filemode = 'w', # -- clear the file contents on each run --
    format = '%(asctime)s | %(levelname)s | %(message)s'
)

#----------------------#
#  Database Connection #
#----------------------#

db_user = 'postgres'
db_pass = 'guptaRia123'
db_host = 'localhost'
db_port = '5433'
db_name = 'salesdb'

engine = create_engine(
    f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
)

#-----------------------#
#       Extract         #
#-----------------------#

try:
    df = pd.read_csv('database/sales_data/sample_data.csv')
    logging.info(f'loaded {len(df)} rows from data file.')
    logging.info(f'first rows are {df.head()} ')
except Exception as e:
    logging.error("Error loading csv file: %s", e)
    raise

#-----------------------#
#      Transform        #
#-----------------------#

try:
    df['total_sales'] = df['quantity'] * df['unit_price']
    df['order_date'] = pd.to_datetime(df['order_date'])
    logging.info("Transformation complete : Sample\n %s",df.head())
except Exception as e:
    logging.info("Transformation complete : %s",e)
    raise

#-----------------------#
#        Load           #
#-----------------------#


try:

   
    df.to_sql(
        'transactions',
        engine,
        schema = 'sales_data',
        if_exists='append',
        index=False
    )
    logging.info("Successfully loaded")
    with engine.connect() as connection:
        result = connection.execute(text(f"Select * from sales_data.transactions"))
        rows = result.fetchall()
        logging.info("total rows in table in sql is %s" ,len(rows))

except Exception as e:
    logging.info("error occured %s",e)
    raise



    

