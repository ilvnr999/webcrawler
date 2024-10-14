from collections import Counter

# 範例 list
my_list = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']

# 使用 Counter 計算每個元素出現的次數
counter = Counter(my_list)

print(dict(counter))
