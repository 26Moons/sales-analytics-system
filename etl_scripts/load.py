import pandas as pd
import psycopg2
from psycopg2 import sql , extras
from etl_scripts.utils import get_logger
from etl_scripts.config_loader import load_config

logger = get_logger("load")
configs = load_config()

def _get_connection(db_conf):
    conn = psycopg2.connect(
        host = db_conf["host"],
        port = db_conf.get("port", 5432),
        user = db_conf["user"],
        password = db_conf["password"],
        dbname = db_conf["name"]
    )
    return conn

def _prepare_rows(df , columns):
    copydf = df.copy()
    copydf = copydf[columns]
    copydf = copydf.where(copydf.notnull(),None)
    return [tuple(r) for r in df.to_numpy()]

def load_to_postgres(df : pd.DataFrame , chunk_size: int = 5000):
    db_conf = configs["database"]
    columns = configs["schema"]["columns"]
    table_name = db_conf["table"]
    

    try:
        logger.info("Connecting to sql db")
        rows = _prepare_rows(df , columns)
        total_rows = len(rows)
        logger.info(f"{rows} rows are prepared for import")


        with _get_connection(db_conf) as conn:
            with conn.cursor() as cur:
                print(conn.dsn)
                try:
                    create_table_query = sql.SQL("""
                        CREATE TABLE IF NOT EXISTS {table} (
                            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            date DATE,
                            region TEXT,
                            product TEXT,
                            sales NUMERIC,
                            quantity INT
                        );
                    """
                    ).format(table=sql.Identifier(table_name))
                    cur.execute(create_table_query)
                    logger.info("Ensured {table_name} exists.")

                    #bulk inserts
                    insert_stmt = sql.SQL("""
                        INSERT INTO {table} ({cols})
                        VALUES %s
                    """).format(
                        table=sql.Identifier(table_name),
                        # table = sql.Identifier(schema , table_name)
                        cols=sql.SQL(", ").join(map(sql.Identifier, columns))
                    )

                    for i in range(0, total_rows, chunk_size):
                        chunk = rows[i:i + chunk_size]
                        extras.execute_values(cur, insert_stmt.as_string(conn), chunk)
                        logger.info(f"Inserted rows {i+1} to {min(i+chunk_size, total_rows)}")
                    
                    

                    query = f"SELECT COUNT(*) FROM {table_name};"
                    cur.execute(query)
                    logger.info("The total no of rows are %s",cur.fetchone()[0])
                    logger.info("The table is %s",table_name)

                except Exception as e:
                    conn.rollback()
                    logger.error(f"❌ Transaction rolled back due to: {e}")
        
                
        logger.info(f"Successfully loaded {total_rows} rows into {table_name}")

        conn.commit()
    except Exception as e:
        logger.exception("Failed to load data into Postgres: %s", e)
        raise