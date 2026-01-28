import sys
import os

# Ensure project root is in Python path (Streamlit-safe)
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd

# -------- Architecture imports --------
from schema.schema_profiler import infer_semantic_type
from pipelines.numeric_pipeline import run_numeric_pipeline
from pipelines.pii_pipeline import run_pii_pipeline
from pipelines.text_pipeline import run_text_pipeline
from pipelines.hybrid_pipeline import merge_outputs

from validation.schema_validator import validate_schema
# from validation.quality_metrics import generate_quality_report


# ------------------ UI CONFIG ------------------
st.set_page_config(
    page_title="Synthetic Data Platform",
    layout="wide"
)

st.title("🧬 Synthetic Data Engine")
st.caption("SDV + GPT + RAG + Faker (Row-coherent & Domain-safe)")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a CSV file to begin.")
    st.stop()

# ------------------ READ INPUT ------------------
try:
    real_df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Failed to read CSV: {e}")
    st.stop()

st.subheader("📄 Real Data Preview")
st.dataframe(real_df.head())

# ------------------ USER INPUT ------------------
num_rows = st.number_input(
    "Number of synthetic rows",
    min_value=10,
    max_value=10000,
    value=100,
    step=10
)

# ------------------ GENERATION ------------------
if st.button("Generate Synthetic Data", type="primary"):

    with st.spinner("Generating synthetic data..."):

        # -------- STEP 1: Schema profiling --------
        try:
            semantic_map = {
                col: infer_semantic_type(real_df[col])
                for col in real_df.columns
            }
        except Exception as e:
            st.error(f"Schema profiling failed: {e}")
            st.stop()

        # -------- STEP 2: Numeric + categorical + date --------
        try:
            numeric_df = run_numeric_pipeline(
                real_df=real_df,
                semantic_map=semantic_map,
                num_rows=num_rows
            )
        except Exception as e:
            st.error(f"Numeric pipeline failed: {e}")
            st.stop()

        # -------- STEP 3: PII (gender-aware) --------
        try:
            pii_data = run_pii_pipeline(
                semantic_map=semantic_map,
                num_rows=num_rows,
                base_df=numeric_df
            )
        except Exception as e:
            st.error(f"PII pipeline failed: {e}")
            st.stop()

        # -------- STEP 4: Merge numeric + PII --------
        try:
            synthetic_df = merge_outputs(
                numeric_df=numeric_df,
                pii_data=pii_data,
                text_data={},  # text added next
                column_order=real_df.columns.tolist()
            )
        except Exception as e:
            st.error(f"Merge (numeric + PII) failed: {e}")
            st.stop()

        # -------- STEP 5: Text (row-aware + length-controlled) --------
        try:
            text_data = run_text_pipeline(
                semantic_map=semantic_map,
                base_df=synthetic_df,   # context
                num_rows=num_rows,
                real_df=real_df         # length learning
            )
        except Exception as e:
            st.error(f"Text pipeline failed: {e}")
            st.stop()

        # -------- STEP 6: Final merge --------
        try:
            synthetic_df = merge_outputs(
                numeric_df=synthetic_df,
                pii_data={},
                text_data=text_data,
                column_order=real_df.columns.tolist()
            )
        except Exception as e:
            st.error(f"Final merge failed: {e}")
            st.stop()

        # -------- STEP 7: Schema validation --------
        try:
            validate_schema(real_df, synthetic_df)
        except Exception as e:
            st.error(f"Schema validation failed: {e}")
            st.stop()

    # ------------------ OUTPUT ------------------
    st.success("✅ Synthetic data generated successfully!")

    st.subheader("🧪 Synthetic Data Preview")
    st.dataframe(synthetic_df.head())

    # ------------------ DOWNLOAD ------------------
    st.download_button(
        label="⬇ Download Synthetic CSV",
        data=synthetic_df.to_csv(index=False),
        file_name="synthetic_data.csv",
        mime="text/csv"
    )
