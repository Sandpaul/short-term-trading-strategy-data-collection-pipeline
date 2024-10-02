def transform_and_clean_data(df):

    transformed_df = df.copy()

    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    missing_columns = [
        col for col in required_columns if col not in transformed_df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    transformed_df = transformed_df.drop_duplicates()
    transformed_df = transformed_df.dropna()
    transformed_df = transformed_df.drop(columns=["Adj Close"])

    columns_to_round = ["Open", "High", "Low", "Close"]
    transformed_df[columns_to_round] = transformed_df[columns_to_round].round(2)

    transformed_df = transformed_df.rename_axis('datetime')
    transformed_df.columns = ['open', 'high', 'low', 'close', 'volume']

    return transformed_df
