import pandas as pd

df = pd.read_csv('csv/line_new2.csv')
# print(df.iloc[112])
print(df['Categories'].to_string())