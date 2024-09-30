import pandas as pd

fn = 'csv/line.csv'
# 讀取 CSV 文件
df = pd.read_csv(fn)

# 提取單個列
column_data = df['Author']
a = set(column_data.tolist())
# 打印提取的列數據

