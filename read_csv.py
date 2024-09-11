import pandas as pd

fn = 'new.csv'
# 讀取 CSV 文件
df = pd.read_csv(fn)

# 提取單個列
column_data = df[['other_picture']]

# 打印提取的列數據
print(column_data)
