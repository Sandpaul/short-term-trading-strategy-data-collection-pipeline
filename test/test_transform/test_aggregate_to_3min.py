import numpy as np
import pandas as pd
import pytest

from src.transform.aggregate_to_3min import aggregate_to_3min


@pytest.fixture
def sample_1min_data():
    data = {
        "open": [42236.09, 42237.00, 42238.00, 42239.00, 42240.00, 42241.00],
        "high": [42237.50, 42238.50, 42239.50, 42240.50, 42241.50, 42242.50],
        "low": [42235.50, 42236.50, 42237.50, 42238.50, 42239.50, 42240.50],
        "close": [42237.00, 42238.00, 42239.00, 42240.00, 42241.00, 42242.00],
        "volume": [100, 150, 200, 250, 300, 350],
    }
    index = pd.date_range(start="2024-09-25 09:30:00", periods=6, freq="min")
    return pd.DataFrame(data, index=index)


@pytest.fixture
def sample_15min_data():
    data = {
        "open": [42236.09, 42237.00, 42238.00, 42239.00, 42240.00, 42241.00],
        "high": [42237.50, 42238.50, 42239.50, 42240.50, 42241.50, 42242.50],
        "low": [42235.50, 42236.50, 42237.50, 42238.50, 42239.50, 42240.50],
        "close": [42237.00, 42238.00, 42239.00, 42240.00, 42241.00, 42242.00],
        "volume": [100, 150, 200, 250, 300, 350],
    }
    index = pd.date_range(start="2024-09-25 09:30:00", periods=6, freq="15min")
    return pd.DataFrame(data, index=index)


def test_aggregate_to_3min_shape(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    assert result.shape[0] == 2
    assert result.shape[1] == 5


def test_aggregate_to_3min_index(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    expected_index = pd.to_datetime(["2024-09-25 09:30:00", "2024-09-25 09:33:00"])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_aggregate_to_3min_open(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    assert result["open"].iloc[0] == 42236.09
    assert result["open"].iloc[1] == 42239.00


def test_aggregate_to_3min_high(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    assert result["high"].iloc[0] == 42239.50
    assert result["high"].iloc[1] == 42242.50


def test_aggregate_to_3min_low(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    assert result["low"].iloc[0] == 42235.50
    assert result["low"].iloc[1] == 42238.50


def test_aggregate_to_3min_close(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    assert result["close"].iloc[0] == 42239.000000
    assert result["close"].iloc[1] == 42242.000000


def test_aggregate_to_3min_volume(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)

    assert result["volume"].iloc[0] == 450
    assert result["volume"].iloc[1] == 900


def test_aggregate_to_3min_returns_new_dataframe(sample_1min_data):
    result = aggregate_to_3min(sample_1min_data)
    assert result is not sample_1min_data


def test_aggregate_to_3min_does_not_mutate_input(sample_1min_data):
    original_data = sample_1min_data
    aggregate_to_3min(sample_1min_data)
    pd.testing.assert_frame_equal(sample_1min_data, original_data, check_dtype=True)


def test_aggregate_to_3min_raises_on_non_datetime_index():
    df = pd.DataFrame(
        {
            "open": [1, 2, 3],
            "high": [1, 2, 3],
            "low": [1, 2, 3],
            "close": [1, 2, 3],
            "volume": [1, 2, 3],
        },
        index=[0, 1, 2],
    )

    with pytest.raises(ValueError, match="The index must be a datetime type."):
        aggregate_to_3min(df)


def test_aggregate_to_3min_raises_on_wrong_frequency(sample_15min_data):
    with pytest.raises(
        ValueError, match="Expected 1-minute data, but got 15min frequency."
    ):
        aggregate_to_3min(sample_15min_data)


def test_aggregate_to_3min_raises_on_time_gaps(sample_1min_data):
    time_jump_row = pd.DataFrame(
        {
            "open": [1],
            "high": [1],
            "low": [1],
            "close": [1],
            "volume": [1],
        },
        index=pd.date_range(start="2024-09-25 09:50:00", periods=1, freq="min"),
    )
    df_with_time_jump = pd.concat([sample_1min_data, time_jump_row])
    df_with_time_jump = df_with_time_jump.sort_index()

    with pytest.raises(
        ValueError, match="The data contains gaps larger than 1 minute."
    ):
        aggregate_to_3min(df_with_time_jump)
