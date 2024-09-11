import csv

# 假設有多個字典，每個字典代表一行數據
data = [
    {'name': 'Alice', 'age': 30, 'city': 'New York'},
    {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
    {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
]

# 確定列名（根據字典的鍵）
fieldnames = ['name', 'age', 'city']

# 打開 CSV 文件並寫入數據
with open('output.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # 寫入列名
    writer.writeheader()
    
    # 寫入數據行
    for row in data:
        writer.writerow(row)
