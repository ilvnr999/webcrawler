import pandas as pd

fn = 'csv/line_new2.csv'
# 讀取 CSV 文件
df = pd.read_csv(fn)

# 提取單個列
column_data = df['Content']
a = column_data.apply(lambda x : x[-250:])
# 打印提取的列數據
for index, an in enumerate(a):
    if '同步追蹤我們的 Google 新聞、LIN' in an:
        print(index, an)
