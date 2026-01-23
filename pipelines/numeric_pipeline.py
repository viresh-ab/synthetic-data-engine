import pandas as pd

def run_numeric_pipeline(real_df, semantic_map, num_rows):
    numeric_cols = []

    for col, sem in semantic_map.items():
        if sem.name.startswith("NUMERIC") or sem.name == "CATEGORICAL":
            numeric_cols.append(col)

    if not numeric_cols:
        return pd.DataFrame(index=range(num_rows))

    df_numeric = real_df[numeric_cols]

    return df_numeric.sample(
        n=num_rows,
        replace=True,
        random_state=42
    ).reset_index(drop=True)
