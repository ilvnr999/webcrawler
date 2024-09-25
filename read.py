import pandas as pd

df = pd.read_csv('ltn.csv')
print(df['Categories'].to_string())