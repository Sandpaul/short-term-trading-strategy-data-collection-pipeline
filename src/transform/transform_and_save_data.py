import logging
from src.transform.transform import transform_and_clean_data
from src.transform.aggregate_to_3min import aggregate_to_3min
from src.utils.read_parquet_from_s3 import read_parquet_from_s3
from src.utils.save_to_s3_as_parquet import save_to_s3_as_parquet


def transform_and_save_data(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info("Function started.")

    try:
        logger.info("Processing event: %s", event)
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_name = event["Records"][0]["s3"]["object"]["key"]
        formatted_file_name = file_name.replace("%3A", "")
        logger.info(f"Bucket: {bucket_name}, File: {file_name}, Formatted File: {formatted_file_name}")

        symbol_interval, date_with_extension = formatted_file_name.split("/")
        symbol, interval = symbol_interval.split("_")
        date = date_with_extension.replace(".parquet", "")
        logger.info(f"Parsed details - Symbol: {symbol}, Interval: {interval}, Date: {date}")

        logger.info(f"Reading parquet file from S3: {formatted_file_name} in bucket: {bucket_name}")
        df = read_parquet_from_s3(bucket_name=bucket_name, file_path=formatted_file_name)
        logger.info(f"Data read successfully. Shape of DataFrame: {df.shape}")

        logger.info("Transforming data.")
        transformed_df = transform_and_clean_data(df)
        logger.info(f"Data transformed successfully. Shape of transformed DataFrame: {transformed_df.shape}")

        data_dict = {
            "data": transformed_df,
            "symbol": symbol,
            "interval": interval,
            "date": date,
        }

        processed_bucket_name = (
            "processed-bucket-st-trading-strategy-data-collection-pipeline"
        )
        logger.info(f"Saving transformed data to S3 bucket: {processed_bucket_name}")
        save_to_s3_as_parquet(bucket_name=processed_bucket_name, data_dict=data_dict)
        logger.info("Data saved successfully.")

        if interval == "1m":
            logger.info("Interval is '1m', aggregating data to 3-minute intervals.")
            three_min_df = aggregate_to_3min(transformed_df)
            logger.info(f"Data aggregated to 3-minute intervals. Shape of 3min DataFrame: {three_min_df.shape}")

            three_min_data_dict = {
                "data": three_min_df,
                "symbol": symbol,
                "interval": "3m",
                "date": date,
            }

            logger.info(f"Saving 3-minute aggregated data to S3 bucket: {processed_bucket_name}")
            save_to_s3_as_parquet(
                bucket_name=processed_bucket_name, data_dict=three_min_data_dict
            )
            logger.info("3-minute aggregated data saved successfully.")
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise e
