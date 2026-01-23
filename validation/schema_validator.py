import pandas as pd

def merge_outputs(
    numeric_df,
    pii_data,
    text_data,
    column_order
):
    df = numeric_df.copy()

    # Add PII columns
    for col, values in pii_data.items():
        df[col] = values

    # Add text columns
    for col, values in text_data.items():
        df[col] = values

    # Reorder columns to match real dataset
    df = df[column_order]

    return df
