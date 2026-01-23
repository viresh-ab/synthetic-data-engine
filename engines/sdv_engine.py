from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

def generate_numeric_data(df_numeric, num_rows):
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df_numeric)

    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(df_numeric)

    synthetic = synthesizer.sample(num_rows)
    return synthetic
