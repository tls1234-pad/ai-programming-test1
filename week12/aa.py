import pandas as pd
from pathlib import Path

df = pd.read_csv(Path(__file__).parent / 'scores_2026.csv')
print(df.shape)