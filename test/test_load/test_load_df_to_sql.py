import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.load.load_df_to_psql import load_df_to_psql


@pytest.fixture()
def sample_df():
    data = {
        "open": [100.0, 101.0],
        "high": [105.0, 106.0],
        "low": [95.0, 96.0],
        "close": [102.0, 103.0],
        "volume": [1000, 1500],
    }
    return pd.DataFrame(data, index=pd.date_range("2024-10-01", periods=2, freq="min"))


@patch("src.load.load_df_to_psql.create_engine")
@patch("pandas.DataFrame.to_sql")
@patch("os.getenv")
@patch("dotenv.load_dotenv")
def test_load_dataframe_to_psql_success(
    mock_load_dotenv, mock_getenv, mock_to_sql, mock_create_engine, sample_df
):
    mock_getenv.side_effect = {
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_pass",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
    }

    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    load_df_to_psql(sample_df, "test_table")

    mock_create_engine.assert_called_once()

    mock_to_sql.assert_called_once_with(
        "test_table", con=mock_engine, if_exists="append", index=False
    )

    mock_create_engine.assert_called_once_with(
        "postgresql+psycopg2://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME"
    )
