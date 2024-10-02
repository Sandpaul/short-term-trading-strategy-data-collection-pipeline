import boto3
from moto import mock_aws
import pandas as pd
import pytest

from src.utils.read_parquet_from_s3 import read_parquet_from_s3


@pytest.fixture(scope="function")
def s3():
    """Create mock s3 client."""
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture
def test_data():
    return pd.DataFrame(
        {
            "Open": [42223.53],
            "High": [42226.32],
            "Low": [42204.78],
            "Close": [42211.37],
            "Adj Close": [42211.37],
            "Volume": [1000],
        }
    )


@pytest.fixture
def test_bucket(s3, test_data):
    """Create mock s3 bucket with parquet file."""
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    data_to_write = pd.DataFrame.to_parquet(test_data)
    s3.put_object(
        Body=data_to_write, Bucket="test-bucket", Key="^DJI_1m/2024-09-30.parquet"
    )


def test_read_parquet_from_s3(s3, test_data, test_bucket):
    bucket_name = "test-bucket"
    file_path = "^DJI_1m/2024-09-30.parquet"
    result = read_parquet_from_s3(bucket_name, file_path)
    expected_data = pd.DataFrame(
        {
            "Open": [42223.53],
            "High": [42226.32],
            "Low": [42204.78],
            "Close": [42211.37],
            "Adj Close": [42211.37],
            "Volume": [1000],
        }
    )
    assert isinstance(result, pd.DataFrame)
    assert result.equals(expected_data)
