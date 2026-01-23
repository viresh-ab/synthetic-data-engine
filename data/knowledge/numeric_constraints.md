# Numeric & Business Constraints (RAG Source)

These constraints are used to validate and correct SDV-generated numeric data.
They ensure realistic and business-appropriate values.

## Age Constraints
- Minimum age: 15 years
- Maximum age: 65 years

## Monthly Fashion Spend (INR)
- Students (Age < 22): ₹500 – ₹3,000
- Early professionals (Age 22–30): ₹1,500 – ₹6,000
- Mid professionals (Age 30–45): ₹2,000 – ₹10,000
- Senior consumers (Age > 45): ₹1,500 – ₹8,000

## Spend vs Income Logic
- Monthly fashion spend should not exceed 20% of monthly income.
- Extremely high spend values should be capped based on age group.

## Purchase Frequency (if applicable)
- Low frequency: 1–2 times per month
- Medium frequency: 3–5 times per month
- High frequency: More than 5 times per month

## Data Sanity Rules
- Numeric values must be non-negative.
- Outliers should be clipped rather than removed.
- Correlations (Age ↔ Spend) should remain logical.

## Enforcement Priority
1. Hard limits (age, non-negative values)
2. Spend caps by age group
3. Income-based percentage limits
