import logging
from src.load.load_df_to_psql import load_df_to_psql
from src.utils.read_parquet_from_s3 import read_parquet_from_s3


def load(event, context):

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_name = event["Records"][0]["s3"]["object"]["key"]
    formatted_file_name = file_name.replace("%3A", "")

    symbol_interval, date_with_extension = formatted_file_name.split("/")
    symbol, interval = symbol_interval.split("_")

    df = read_parquet_from_s3(bucket_name=bucket_name, file_path=formatted_file_name)

    table_name = f"{symbol}-{interval}"

    load_df_to_psql(table_name=table_name, df=df)
