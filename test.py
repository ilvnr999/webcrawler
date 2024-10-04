data = {
    "name": ['a', 'b', 'c'],
    "name2": ['d', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
}

for key, value in data.items():
    print(value)
    '''for i in range(0, len(value), 5):
        # 取出當前範圍內的5個元素 (或不足5個的剩餘元素)
        chunk = value[i:i + 5]
        print(f"{key} - {chunk}")'''