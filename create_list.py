import pandas as pd

# 讀取檔案
df = pd.read_csv("tech_news/terms.csv")
noun = df['名詞']
df['數量'] = None

for i, n in enumerate(noun):
    if 'A' <= n <= 'Z' or 'a' <= n <= 'z':
        continue
    else:
        df.iat[i, 1] = df.iat[i, 0]
        df.iat[i, 0] = None
df.columns = ['英文', '繁中']
df.to_csv('tech_news/list.csv', index=False)