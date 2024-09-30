import csv

import requests
from bs4 import BeautifulSoup

from line_url import fetch

url_content = []
fieldnames =[]
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

    target_divs = soup.find_all('div', attrs={'data-anchor-id': True})

    # 遍歷每個 <div>，並查找其內部的 <h2>
    for div in target_divs:
        h2_tag = div.find('h2')  # 查找內部的 <h2>
        if h2_tag:
            h2 = '理財' + h2_tag.text.strip()
        else:
            h2 = '理財'

        #print(h2)  # 輸出 data-anchor-id 和 h2 的文本內容
        links = div.find_all('a', class_='ltcp-link')  # 在 <h2> 中查找所有 class 為 ltcp-link 的 <a>
        if links:  # 如果找到一個或多個 <a>
            hrefs = [link['href'] for link in links ]  # 獲取所有 href 值
            for href in hrefs:
                if 'article' in href :
                    if '60VLrQw' in href:
                        continue
                    url = 'https://today.line.me' + href
                    output = fetch(url, h2)
                    if output != 0:
                        url_content.append(output)
                    print(output)

    # 讀取行名稱
    fieldnames = list(url_content[0].keys())
    print('column names',fieldnames)

    csv_name = 'csv/line_api.csv'
    with open(csv_name, 'w', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in url_content:
            writer.writerow(row)

if __name__ == '__main__':
    grab()