import sys
import os
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd

# --- Imports from your architecture ---
from schema.schema_profiler import infer_semantic_type
from pipelines.numeric_pipeline import run_numeric_pipeline
from pipelines.pii_pipeline import run_pii_pipeline
from pipelines.text_pipeline import run_text_pipeline
from pipelines.hybrid_pipeline import merge_outputs

st.set_page_config(page_title="Synthetic Data Platform", layout="wide")

st.title("🧬 Hybrid Synthetic Data Generator")
st.write("SDV + GPT LLM + RAG + Faker")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    real_df = pd.read_csv(uploaded_file)
    st.subheader("Real Data Preview")
    st.dataframe(real_df.head())

    num_rows = st.number_input(
        "Number of synthetic rows",
        min_value=10,
        max_value=10000,
        value=100
    )

    if st.button("Generate Synthetic Data"):
        with st.spinner("Generating synthetic data..."):

            # STEP 1: Semantic schema
            semantic_map = {
                col: infer_semantic_type(real_df[col])
                for col in real_df.columns
            }

            # STEP 2: Numeric pipeline (SDV + RAG)
            numeric_df = run_numeric_pipeline(
                real_df, semantic_map, num_rows
            )

            # STEP 3: PII pipeline (Faker)
            pii_data = run_pii_pipeline(
                semantic_map, num_rows
            )

            # STEP 4: Text pipeline (GPT LLM)
            text_data = run_text_pipeline(
                semantic_map,
                real_df,
                num_rows
            )

            # STEP 5: Merge everything
            synthetic_df = merge_outputs(
                numeric_df,
                pii_data,
                text_data,
                column_order=real_df.columns.tolist()
            )

            st.success("Synthetic data generated successfully!")

            st.subheader("Synthetic Data Preview")
            st.dataframe(synthetic_df.head())

            st.download_button(
                "Download Synthetic CSV",
                synthetic_df.to_csv(index=False),
                file_name="synthetic_data.csv",
                mime="text/csv"
            )
