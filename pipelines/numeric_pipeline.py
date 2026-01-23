from engines.sdv_engine import generate_numeric_data
from engines.rag_engine import fetch_constraints
from engines.rule_engine import apply_numeric_rules

def run_numeric_pipeline(real_df, semantic_map, num_rows):
    # 1️⃣ Select numeric columns only
    numeric_cols = [
        col for col, t in semantic_map.items()
        if t.name.startswith("NUMERIC") or t.name == "CATEGORICAL"
    ]

    df_numeric = real_df[numeric_cols]

    # 2️⃣ Generate with SDV
    synthetic_numeric = generate_numeric_data(df_numeric, num_rows)

    # 3️⃣ Fetch RAG constraints
    constraints = fetch_constraints(context="fashion_india")

    # 4️⃣ Apply rules
    synthetic_numeric = apply_numeric_rules(
        synthetic_numeric,
        constraints
    )

    return synthetic_numeric

if df_numeric.empty:
    return pd.DataFrame(index=range(num_rows))
