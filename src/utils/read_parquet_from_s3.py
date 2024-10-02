import io

import pandas as pd
import boto3


def read_parquet_from_s3(bucket_name, file_path):

    s3 = boto3.client("s3")

    response = s3.get_object(Bucket=bucket_name, Key=file_path)

    file_contents = response["Body"].read()
    content_in_bytes = io.BytesIO(file_contents)
    df = pd.read_parquet(content_in_bytes)

    return df
