"""This module contains the definition for `extract_data()`."""

import yfinance as yf

def extract_data(symbol, interval):
    """Extracts one day's worth of data from the Yahoo Finance API.

    Args:
        symbol (string): a valid ticket symbol, e.g. '^DJI'
        interval (string): a time interval, e.g. '1m', '15m', or '1h'

    Returns:
        dataFrame: a dataFrame of the retrieved data
    """
    data = yf.download(tickers=symbol, period='1d', interval=interval)
    return data

if __name__ == "__main__":
    dow_1min_data = extract_data('^DJI', '1m')
    dow_15min_data = extract_data('^DJI', '15m')
    dow_1hr_data = extract_data('^DJI', '1h')