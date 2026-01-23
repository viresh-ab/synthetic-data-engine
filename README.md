# 🚀 Synthetic Data Engine
A production-ready **hybrid synthetic data generator** that combines multiple engines to produce **accurate, diverse, and privacy-safe synthetic datasets**.

### Core Technologies
- **SDV** → Numeric & categorical statistical realism  
- **GPT LLMs** → Natural language & survey responses  
- **RAG** → Business & domain constraints  
- **Faker** → Privacy-safe identity (PII) generation  

---

## 🚀 Features

- Semantic column understanding (not just data types)
- Privacy-safe PII handling (no memorization or reuse)
- Non-repetitive, persona-driven text generation
- Business-rule-aware numeric synthesis
- Modular, extensible architecture
- Streamlit UI for easy usage

---

## 🚀 Architecture Overview

| Data Type | Engine Used |
|---------|------------|
| Numeric & categorical | SDV + RAG |
| Names / Emails / IDs | Faker |
| Text / Q&A / Opinions | GPT LLM |
| Validation | Rule Engine + Quality Metrics |

---

## 🚀 High-Level System Architecture

```text
                ┌───────────────┐
                │  Real Dataset │
                └───────┬───────┘
                        │
                ┌───────▼────────┐
                │ Schema Profiler │
                └───────┬────────┘
                        │
     ┌──────────────────┼──────────────────┐
     │                  │                  │
┌────▼────┐        ┌────▼────┐        ┌────▼────┐
│ SDV     │        │ RAG     │        │ Faker   │
│ Engine  │        │ Engine  │        │ Engine  │
│ (Stats) │        │ (Rules) │        │ (PII)   │
└────┬────┘        └────┬────┘        └────┬────┘
     │                  │                  │
     └──────────┬───────┴───────┬──────────┘
                │               │
        ┌───────▼───────┐  ┌────▼────────┐
        │ GPT LLM Engine │  │ Validator   │
        │ (Text / Q&A)   │  │ & Merger    │
        └───────┬───────┘  └────┬────────┘
                │               │
                └───────┬───────┘
                        ▼
                ┌────────────────┐
                │ Synthetic Data │
                └────────────────┘
```
---

## 🚀 SDE File Structure
```text
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

