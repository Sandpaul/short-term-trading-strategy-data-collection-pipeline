import re
import numpy as np
import pandas as pd
import pytest


from src.transform.transform import transform_and_clean_data


@pytest.fixture
def sample_data():
    """Fixture to provide sample DataFrame for testing."""
    data = {
        "Open": [42236.089844, 42295.761719, 42198.679688],
        "High": [42299.640625, 42296.558594, 42259.781250],
        "Low": [42236.089844, 42199.230469, 42198.679688],
        "Close": [42287.621094, 42200.648438, 42259.398438],
        "Volume": [0, 1527434, 1529194],
        "Adj Close": [42287.621094, 42200.648438, 42259.398438],
    }
    index = pd.to_datetime(
        ["2024-09-25 09:30:00", "2024-09-25 09:31:00", "2024-09-25 09:32:00"]
    )
    df = pd.DataFrame(data, index=index)
    return df


def test_transform_and_clean_data_drops_adj_close(sample_data):
    result = transform_and_clean_data(sample_data)
    expected_columns = ["open", "high", "low", "close", "volume"]
    assert list(result.columns) == expected_columns


def test_transform_and_clean_data_rounds_numeric_columns_and_renames_columns(
    sample_data,
):
    result = transform_and_clean_data(sample_data)
    expected_data = {
        "open": [42236.09, 42295.76, 42198.68],
        "high": [42299.64, 42296.56, 42259.78],
        "low": [42236.09, 42199.23, 42198.68],
        "close": [42287.62, 42200.65, 42259.40],
        "volume": [0, 1527434, 1529194],
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)


def test_transform_and_clean_data_missing_columns(sample_data):
    df_missing_column = sample_data.drop(columns=["Open"])

    with pytest.raises(
        ValueError, match=re.escape("Missing required columns: ['Open']")
    ):
        transform_and_clean_data(df_missing_column)


def test_transform_and_clean_data_drops_duplicates(sample_data):
    df_with_duplicates = pd.concat([sample_data, sample_data])
    result = transform_and_clean_data(df_with_duplicates)

    assert len(result) == len(sample_data)


def test_transform_and_clean_data_drops_nan_values(sample_data):
    nan_row = pd.DataFrame(
        {
            "Open": [np.nan],
            "High": [np.nan],
            "Low": [np.nan],
            "Close": [np.nan],
            "Volume": [np.nan],
            "Adj Close": [np.nan],
        }
    )
    df_with_nan = pd.concat([sample_data, nan_row], ignore_index=True)
    result = transform_and_clean_data(df_with_nan)

    assert len(result) == len(sample_data)


def test_transform_and_clean_data_renames_index(sample_data):
    result = transform_and_clean_data(sample_data)
    assert result.index.name == "datetime"


def test_transform_and_clean_data_returns_new_dataframe(sample_data):
    result = transform_and_clean_data(sample_data)
    assert result is not sample_data


def test_transform_and_clean_data_does_not_mutate_input(sample_data):
    original_data = sample_data.copy()

    transform_and_clean_data(sample_data)

    pd.testing.assert_frame_equal(sample_data, original_data, check_dtype=True)
