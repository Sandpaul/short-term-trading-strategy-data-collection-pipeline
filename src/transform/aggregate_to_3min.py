import pandas as pd


def aggregate_to_3min(df):
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        raise ValueError("The index must be a datetime type.")

    freq = pd.infer_freq(df.index)

    if freq != "min":
        if freq is None:
            raise ValueError("The data contains gaps larger than 1 minute.")
        else:
            raise ValueError(f"Expected 1-minute data, but got {freq} frequency.")

    aggregated_df = df.resample("3min").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )

    aggregated_df.dropna(inplace=True)

    return aggregated_df
