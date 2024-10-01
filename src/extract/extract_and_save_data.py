from src.extract.extract import extract_data
from src.utils.save_to_s3_as_parquet import save_to_s3_as_parquet


def extract_and_save_data(symbol, intervals, bucket_name):

    for interval in intervals:
        try:
            data = extract_data(symbol, interval)

            save_to_s3_as_parquet(data, bucket_name)

            print(
                f"Successfully processed and saved data for {symbol} at {interval} interval."
            )

        except Exception as e:
            print(f"Error processing data for {symbol} at {interval} interval: {e}")


if __name__ == "__main__":
    BUCKET_NAME = "ingestion-bucket-st-trading-strategy-data-collection-pipeline"
    SYMBOL = "^DJI"
    INTERVALS = ["1m", "15m", "1h"]

    extract_and_save_data(SYMBOL, INTERVALS, BUCKET_NAME)
