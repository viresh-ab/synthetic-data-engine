from scipy.stats import ks_2samp

def numeric_similarity(real, synthetic):
    score = {}
    for col in real.select_dtypes(include="number"):
        ks = ks_2samp(real[col], synthetic[col]).statistic
        score[col] = round(1 - ks, 3)
    return score

def text_diversity(text_series):
    unique_ratio = text_series.nunique() / len(text_series)
    return round(unique_ratio, 3)

def pii_uniqueness(series):
    return round(series.nunique() / len(series), 3)

def generate_quality_report(real_df, synthetic_df):
    return {
        "numeric_similarity": numeric_similarity(real_df, synthetic_df),
        "text_diversity": {
            col: text_diversity(synthetic_df[col])
            for col in synthetic_df.select_dtypes(include="object")
        }
    }
