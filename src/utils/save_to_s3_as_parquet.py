import logging
import pandas as pd
import boto3


def save_to_s3_as_parquet(data_dict, bucket_name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    s3_client = boto3.client("s3")

    parquet_file = pd.DataFrame.to_parquet(data_dict["data"])

    table_name = f"{data_dict['symbol']}_{data_dict['interval']}"

    s3_client.put_object(
        Body=parquet_file,
        Bucket=bucket_name,
        Key=f"{table_name}/{data_dict["date"]}.parquet",
    )

    logger.info(f"{table_name}/{data_dict["date"]}.parquet successfully created")
