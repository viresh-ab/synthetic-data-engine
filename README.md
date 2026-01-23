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

## ▶ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
