"""This module contains the test suite for `extract_data()`."""

from unittest.mock import patch
import pandas as pd
from pandas.testing import assert_frame_equal
from src.extract.extract import extract_data


mock_data = pd.DataFrame({
        'Open': [42223.531250],
        'High': [42226.320312],
        'Low': [42204.781250],
        'Close': [42211.378906],
        'Adj Close': [42211.378906],
        'Volume': [0]
    }, index=pd.to_datetime(['2024-09-30 09:30:00-04:00']))


@patch('yfinance.download')
def test_extract_data(mock_download):
    """test extract_data() returns the mock data and is called once with the correct arguments."""
    mock_download.return_value = mock_data

    symbol = '^DJI'
    interval = '1m'

    result = extract_data(symbol, interval)

    assert_frame_equal(result, mock_data)
    mock_download.assert_called_once_with(tickers=symbol, period='1d', interval=interval)
