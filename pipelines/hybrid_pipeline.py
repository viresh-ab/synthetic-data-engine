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
    # Keep only columns that actually exist
    final_cols = [c for c in column_order if c in df.columns]

    df = df[final_cols]


    return df
