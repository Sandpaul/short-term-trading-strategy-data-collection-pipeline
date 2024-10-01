import pandas as pd
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError


def save_to_s3_as_parquet(data_dict, bucket_name):
    try:

        if not isinstance(data_dict, dict):
            raise TypeError("Input data must be a dictionary")

        required_keys = ["data", "symbol", "interval", "date"]
        for key in required_keys:
            if key not in data_dict:
                raise KeyError(f"Missing key in data_dict: {key}")

        data = data_dict["data"]
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The 'data' field must be a pandas DataFrame.")

        symbol = data_dict["symbol"]
        interval = data_dict["interval"]
        date = data_dict["date"]

        s3_client = boto3.client("s3")

        parquet_file = pd.DataFrame.to_parquet(data)

        s3_key = f"{symbol}_{interval}/{date}.parquet"

        s3_client.put_object(
            Body=parquet_file,
            Bucket=bucket_name,
            Key=s3_key,
        )

        print(f"Successfully saved {s3_key} to bucket {bucket_name}")

    except TypeError as te:
        raise te

    except KeyError as ke:
        raise ke

    except (BotoCoreError, NoCredentialsError, ClientError) as s3_error:
        raise s3_error

    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
