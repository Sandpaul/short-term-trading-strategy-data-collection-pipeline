"""This module contains the test suite for `extract_data()`."""

from unittest.mock import patch
import pandas as pd
import pytest
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

    assert isinstance(result, pd.DataFrame)
    mock_download.assert_called_once_with(tickers=symbol, period='1d', interval=interval)


@patch('yfinance.download')
def test_extract_data_value_error(mock_download):
    """test extract_data() raises a value error when returned DataFrame is empty"""

    mock_download.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="No data found for symbol"):
        extract_data('^DJI', '1m')


@patch('yfinance.download')
def test_extract_data_exception(mock_download):
    """test extract_data() catches any other exceptions and raises them"""

    mock_download.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="Error fetching data for"):
        extract_data('^DJI', '1m')
