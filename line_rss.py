import csv

import requests
from bs4 import BeautifulSoup

from line_url import fetch


def grab():
    # 指定RSS feed的URL
    url = 'https://today.line.me/tw/v3/page/finance'

    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=("bbc1a2b309d74e21a8cc452e054e54d5", ""),
        json={
            "url": url,
            "browserHtml": True,
        },
    )
    if api_response.status_code != 200:  # 狀態不為200跳出
        return print(f'{url} \n status = {api_response.status_code}')
    
    browser_html: str = api_response.json()["browserHtml"]
    if browser_html:
        soup = BeautifulSoup(browser_html, 'html5lib')

    h2 = soup.find_all('a', class_='ltcp-link')
    links = [h.get('href') for h in h2]


    for link in links:
        if '/tw/v2/article/' in str(link):
            str1 = 'https://today.line.me' + link
            print(fetch(str1))

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