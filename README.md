# 🧬 Hybrid Synthetic Data Platform

A production-ready synthetic data generator that combines:

- **SDV** → Numeric & categorical realism
- **GPT LLMs** → Natural language & survey responses
- **RAG** → Business & domain constraints
- **Faker** → Privacy-safe identity generation

---

## 🚀 Features

- Semantic column understanding
- Privacy-safe PII handling
- Non-repetitive text generation
- Business-rule-aware numeric synthesis
- Streamlit UI for easy usage

---

## 🏗 Architecture Overview

| Data Type | Engine Used |
|---------|------------|
Numeric & categorical | SDV + RAG |
Names / Emails / IDs | Faker |
Text / Q&A / Opinions | GPT LLM |
Validation | Rule + Quality Metrics |

---

## 🏗 File Structure

synthetic-data-platform/
│
├── app.py                    # Streamlit / API entry point
├── config.yaml               # Global configuration
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
│
├── schema/                   # Step 1: Schema understanding
│   ├── schema_profiler.py    # Semantic column classification
│   ├── column_types.py       # Semantic type definitions
│   └── pii_detector.py       # PII identification logic
│
├── engines/                  # Core generation engines
│   ├── sdv_engine.py         # SDV-based numeric synthesis
│   ├── llm_engine.py         # GPT LLM text generation
│   ├── rag_engine.py         # RAG constraint retrieval
│   ├── faker_engine.py       # PII & identity generation
│   └── rule_engine.py        # Business rule enforcement
│
├── pipelines/                # Orchestration layers
│   ├── numeric_pipeline.py   # SDV + RAG numeric pipeline
│   ├── text_pipeline.py      # GPT text & persona pipeline
│   ├── pii_pipeline.py       # Faker-based PII pipeline
│   └── hybrid_pipeline.py    # Final merge pipeline
│
├── prompts/                  # LLM prompt assets
│   ├── base_prompt.txt       # Global LLM rules
│   ├── fashion_personas.json # Persona definitions
│   └── column_prompts.yaml   # Column-specific instructions
│
├── validation/               # Quality & safety checks
│   ├── schema_validator.py   # Schema alignment
│   ├── rule_validator.py     # Business rule validation
│   └── quality_metrics.py    # Similarity & diversity metrics
│
└── .streamlit/
    └── config.toml           # UI theme & layout

---

flowchart TD
    A[Real Input CSV] --> B[Schema Profiler<br/>Semantic Typing]

    B --> C1[Numeric Pipeline<br/>SDV + RAG]
    B --> C2[Text Pipeline<br/>GPT LLM + Personas]
    B --> C3[PII Pipeline<br/>Faker]

    C1 --> D[Hybrid Merger]
    C2 --> D
    C3 --> D

    D --> E[Validation Layer<br/>Schema + Rules]
    E --> F[Quality Metrics<br/>Similarity & Diversity]

    F --> G[Final Synthetic Dataset<br/>CSV Output]




## ▶ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
