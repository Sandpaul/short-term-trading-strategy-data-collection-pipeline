from io import BytesIO
import boto3
from moto import mock_aws
import pandas as pd
import pytest
from src.utils.save_to_s3_as_parquet import save_to_s3_as_parquet


@pytest.fixture(scope="function")
def s3():
    """Create mock s3 client."""
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture
def test_bucket(s3):
    """Create mock s3 bucket."""
    return s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


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
def test_dict(test_data):
    return {"data": test_data, "symbol": "^DJI", "interval": "1m", "date": "2024-09-30"}


def test_save_to_s3_as_parquet_success(s3, test_dict, test_bucket):
    response_1 = s3.list_objects_v2(Bucket="test-bucket")
    assert response_1["KeyCount"] == 0

    save_to_s3_as_parquet(test_dict, "test-bucket")

    response_2 = s3.list_objects_v2(Bucket="test-bucket")
    assert response_2["KeyCount"] == 1


def test_save_to_s3_as_parquet_correct_filename(s3, test_dict, test_bucket):
    save_to_s3_as_parquet(test_dict, "test-bucket")

    response = s3.list_objects_v2(Bucket="test-bucket")
    assert response["Contents"][0]["Key"] == "^DJI_1m/2024-09-30.parquet"


def test_save_to_s3_as_parquet_correct_data(s3, test_dict, test_bucket):
    save_to_s3_as_parquet(test_dict, "test-bucket")

    response = s3.get_object(Bucket="test-bucket", Key="^DJI_1m/2024-09-30.parquet")

    parquet_content = BytesIO(response["Body"].read())
    df_from_s3 = pd.read_parquet(parquet_content)

    pd.testing.assert_frame_equal(test_dict["data"], df_from_s3)


def test_save_to_s3_as_parquet_invalid_data_type():
    invalid_data = "not a dict"
    with pytest.raises(TypeError, match="Input data must be a dictionary"):
        save_to_s3_as_parquet(invalid_data, "test-bucket")


def test_save_to_s3_as_parquet_invalid_dataframe_type():
    invalid_data_dict = {
        "data": "not_a_dataframe",
        "symbol": "^DJI",
        "interval": "1m",
        "date": "2024-09-30",
    }
    with pytest.raises(TypeError, match="The 'data' field must be a pandas DataFrame"):
        save_to_s3_as_parquet(invalid_data_dict, "test-bucket")


def test_save_to_s3_as_parquet_missing_key():
    missing_key_dict = {"data": pd.DataFrame(), "symbol": "^DJI", "interval": "1m"}
    with pytest.raises(KeyError, match="Missing key in data_dict: date"):
        save_to_s3_as_parquet(missing_key_dict, "test-bucket")
