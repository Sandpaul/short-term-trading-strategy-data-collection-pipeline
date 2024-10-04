import boto3
import pytest
from moto import mock_aws
import pandas as pd
import os
from io import BytesIO

from src.transform.transform_and_save_data import transform_and_save_data
from src.utils.read_parquet_from_s3 import read_parquet_from_s3
from src.utils.save_to_s3_as_parquet import save_to_s3_as_parquet


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Open": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0],
            "High": [101.0, 102.0, 103.0, 104.0, 105.0, 106.0],
            "Low": [99.0, 100.0, 101.0, 102.0, 103.0, 104.0],
            "Close": [100.5, 101.5, 102.5, 103.5, 104.5, 105.5],
            "Volume": [1000, 1100, 1200, 1300, 1400, 1500],
            "Adj Close": [1, 1, 1, 1, 1, 1],
        },
        index=pd.date_range(start="2024-10-01 09:30:00", periods=6, freq="min"),
    )


@pytest.fixture
def mock_s3_bucket(sample_data):
    with mock_aws():
        s3_client = boto3.client("s3", region_name="us-east-1")

        ingestion_bucket = "ingestion-bucket"
        s3_client.create_bucket(Bucket=ingestion_bucket)
        data_to_write = pd.DataFrame.to_parquet(sample_data)
        s3_client.put_object(
            Body=data_to_write,
            Bucket=ingestion_bucket,
            Key="^DJI_1m/2024-10-01.parquet",
        )

        processed_bucket = (
            "processed-bucket-st-trading-strategy-data-collection-pipeline"
        )
        s3_client.create_bucket(Bucket=processed_bucket)

        yield s3_client, ingestion_bucket, processed_bucket


@pytest.fixture
def mock_event():
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "ingestion-bucket"},
                    "object": {"key": "^DJI_1m/2024-10-01.parquet"},
                }
            }
        ]
    }


@pytest.fixture
def mock_context():
    return {}


def test_transform_and_save_data(mock_s3_bucket, mock_event, mock_context):
    s3_client, ingestion_bucket, processed_bucket = mock_s3_bucket

    response_1 = s3_client.list_objects_v2(Bucket=processed_bucket)
    assert response_1["KeyCount"] == 0

    transform_and_save_data(event=mock_event, context=mock_context)

    response_2 = s3_client.list_objects_v2(Bucket=processed_bucket)
    assert response_2["KeyCount"] == 2


def test_transform_and_save_data_correct_file_names(
    mock_s3_bucket, mock_event, mock_context
):
    s3_client, ingestion_bucket, processed_bucket = mock_s3_bucket

    transform_and_save_data(event=mock_event, context=mock_context)

    response = s3_client.list_objects_v2(Bucket=processed_bucket)

    assert response["Contents"][0]["Key"] == "^DJI_1m/2024-10-01.parquet"
    assert response["Contents"][1]["Key"] == "^DJI_3m/2024-10-01.parquet"


def test_transform_and_save_data_correct_1min_data(
    mock_s3_bucket, mock_event, mock_context
):
    s3_client, ingestion_bucket, processed_bucket = mock_s3_bucket

    transform_and_save_data(event=mock_event, context=mock_context)

    response = s3_client.get_object(
        Bucket=processed_bucket, Key="^DJI_1m/2024-10-01.parquet"
    )

    expected_content = pd.DataFrame(
        {
            "open": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0],
            "high": [101.0, 102.0, 103.0, 104.0, 105.0, 106.0],
            "low": [99.0, 100.0, 101.0, 102.0, 103.0, 104.0],
            "close": [100.5, 101.5, 102.5, 103.5, 104.5, 105.5],
            "volume": [1000, 1100, 1200, 1300, 1400, 1500],
        },
        index=pd.date_range(start="2024-10-01 09:30:00", periods=6, freq="min"),
    )
    expected_content = expected_content.rename_axis("datetime")

    parquet_content = BytesIO(response["Body"].read())
    df_from_s3 = pd.read_parquet(parquet_content)

    pd.testing.assert_frame_equal(
        df_from_s3, expected_content, check_dtype=True, check_like=True
    )


def test_transform_and_save_data_correct_3min_data(
    mock_s3_bucket, mock_event, mock_context
):
    s3_client, ingestion_bucket, processed_bucket = mock_s3_bucket

    transform_and_save_data(event=mock_event, context=mock_context)

    response = s3_client.get_object(
        Bucket=processed_bucket, Key="^DJI_3m/2024-10-01.parquet"
    )

    expected_content = pd.DataFrame(
        {
            "open": [100.0, 103.0],
            "high": [103.0, 106.0],
            "low": [99.0, 102.0],
            "close": [102.5, 105.5],
            "volume": [3300, 4200],
        },
        index=pd.date_range(start="2024-10-01 09:30:00", periods=2, freq="3min"),
    )
    expected_content = expected_content.rename_axis("datetime")

    parquet_content = BytesIO(response["Body"].read())
    df_from_s3 = pd.read_parquet(parquet_content)

    pd.testing.assert_frame_equal(
        df_from_s3, expected_content, check_dtype=True, check_like=True
    )
