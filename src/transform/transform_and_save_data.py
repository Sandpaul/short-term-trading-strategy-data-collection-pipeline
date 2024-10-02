from src.transform.transform import transform_and_clean_data
from src.transform.aggregate_to_3min import aggregate_to_3min
from src.utils.read_parquet_from_s3 import read_parquet_from_s3
from src.utils.save_to_s3_as_parquet import save_to_s3_as_parquet


def transform_and_save_data(event, context):

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_name = event["Records"][0]["s3"]["object"]["key"]
    formatted_file_name = file_name.replace("%3A", "")

    symbol_interval, date_with_extension = formatted_file_name.split("/")
    symbol, interval = symbol_interval.split("_")
    date = date_with_extension.replace(".parquet", "")

    df = read_parquet_from_s3(bucket_name=bucket_name, file_path=formatted_file_name)

    transformed_df = transform_and_clean_data(df)
    data_dict = {
        "data": transformed_df,
        "symbol": symbol,
        "interval": interval,
        "date": date,
    }

    processed_bucket_name = (
        "processed-bucket-st-trading-strategy-data-collection-pipeline"
    )
    save_to_s3_as_parquet(bucket_name=processed_bucket_name, data_dict=data_dict)

    if interval == "1m":
        three_min_df = aggregate_to_3min(transformed_df)
        three_min_data_dict = {
            "data": three_min_df,
            "symbol": symbol,
            "interval": "3m",
            "date": date,
        }
        save_to_s3_as_parquet(
            bucket_name=processed_bucket_name, data_dict=three_min_data_dict
        )
