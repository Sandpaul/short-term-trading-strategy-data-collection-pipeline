import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


def load_df_to_psql(df, table_name):
    load_dotenv()

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    connection_string = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    )
    engine = create_engine(connection_string)

    try:
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f"DataFrame added to table '{table_name}' successfully")

    except Exception as e:
        print(f"Error while adding DataFrame to table '{table_name}': {e}")

    finally:
        engine.dispose()


def sample_df():
    data = {
        "open": [100.0, 101.0],
        "high": [105.0, 106.0],
        "low": [95.0, 96.0],
        "close": [102.0, 103.0],
        "volume": [1000, 1500],
    }
    return pd.DataFrame(data, index=pd.date_range("2024-10-01", periods=2, freq="min"))


df = sample_df()

load_df_to_psql(df, "^DJI-1m")
load_df_to_psql(df, "^DJI-3m")
