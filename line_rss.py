import csv

import requests
from bs4 import BeautifulSoup

from line_url import fetch


def grab():
    # 指定RSS feed的URL
    url = 'https://today.line.me/tw/v3/page/finance'

    response = requests.get(url)
    print(response.status_code)
    if response.status_code != 200:  # 狀態不為200跳出
        return print(f'{url} \n status = {response.status_code}')
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html5lib')
    article = soup.find('div', id = 'css-rl8tfl')
    div = soup.find_all('div',class_='css-rl8tfl')
    print(div)

    '''# 讀取內容
    for url in url_list:
        content = fetch(url)
        if content ==  0:
            continue
        url_content.append(content)
    
    # 讀取行名稱
    first_dict = url_content[0]
    for key in first_dict:
        fieldnames.append(key)
    print('column names',fieldnames)

    csv_name = 'ltn.csv'
    with open(csv_name, 'w', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in url_content:
            writer.writerow(row)'''

if __name__ == '__main__':
    grab()