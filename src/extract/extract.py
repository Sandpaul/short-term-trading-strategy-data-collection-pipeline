"""This module contains the definition for `extract_data()`."""

import yfinance as yf

from src.utils.save_to_s3_as_parquet import save_to_s3_as_parquet


def extract_data(symbol, interval):
    """Extracts one day's worth of data from the Yahoo Finance API.

    Args:
        symbol (string): a valid ticket symbol, e.g. '^DJI'
        interval (string): a time interval, e.g. '1m', '15m', or '1h'

    Returns:
        dataFrame: a dataFrame of the retrieved data

    Raises:
        ValueError: if no data is returned
        Exception: if there is an issue with the API call
    """
    try:
        data = yf.download(tickers=symbol, period="1d", interval=interval)

        if data.empty:
            raise ValueError(
                f"No data found for symbol: {symbol} with interval: {interval}"
            )

        date = data.index[0].strftime("%Y-%m-%d")

        return {"symbol": symbol, "interval": interval, "date": date, "data": data}

    except ValueError:
        raise
    except Exception as e:
        raise Exception(
            f"Error fetching data for {symbol} at interval {interval}: {e}"
        ) from e


if __name__ == "__main__":
    dow_1min_data = extract_data("^DJI", "1m")
    dow_15min_data = extract_data("^DJI", "15m")
    dow_1hr_data = extract_data("^DJI", "1h")

    BUCKET_NAME = "ingestion-bucket-st-trading-strategy-data-collection-pipeline"

    save_to_s3_as_parquet(dow_1min_data, BUCKET_NAME)
    save_to_s3_as_parquet(dow_15min_data, BUCKET_NAME)
    save_to_s3_as_parquet(dow_1hr_data, BUCKET_NAME)
