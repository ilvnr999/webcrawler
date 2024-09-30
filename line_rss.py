import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from line_url import fetch


def grab(cat, url):
    # 設定 WebDriver
    driver = webdriver.Chrome()  # 確保你已經安裝了 ChromeDriver
    driver.get(url)
    # 模擬滾動到頁面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待頁面加載
    time.sleep(1)  # 可以根據需要調整這個時間
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    target_divs = soup.find_all('div', attrs={'data-anchor-id': True})

    # 遍歷每個 <div>，並查找其內部的 <h2>
    for div in target_divs:
        h2_tag = div.find('h2')  # 查找內部的 <h2>
        if h2_tag:
            h2 = cat + h2_tag.text.strip()
        else:
            h2 = cat

        if h2 not in rss:
            rss[h2] = []

        #print(h2)  # 輸出 data-anchor-id 和 h2 的文本內容
        links = div.find_all('a', class_='ltcp-link')  # 在 <h2> 中查找所有 class 為 ltcp-link 的 <a>
        if links:  # 如果找到一個或多個 <a>
            for link in links:
                half_url = link['href']
                if 'article' in half_url:
                    url = 'https://today.line.me' + half_url
                    rss[h2].append(url)


            '''hrefs = [link['href'] for link in links ]  # 獲取所有 href 值
            print(h2, hrefs)
            for href in hrefs:
                if 'article' in href :
                    url = 'https://today.line.me' + href
                    #output = fetch(url, h2)
                    if output != 0:
                        url_content.append(output)
                    print(output)'''
    driver.quit()

def read_url():
    for cat, urls in rss.items():
        for url in urls:
            output = fetch(url, cat)
            if output != 0:
                url_content.append(output)

def save(): 
    # 讀取行名稱
    fieldnames = list(url_content[0].keys())
    print('column names',fieldnames)

    csv_name = 'csv/line_new.csv'
    with open(csv_name, 'w', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in url_content:
            writer.writerow(row)

if __name__ == '__main__':
    rss = {}
    url_content = []
    url1 = 'https://today.line.me/tw/v3/page/finance'
    grab('理財,' ,url1)
    url2 = 'https://today.line.me/tw/v3/page/tech'
    grab('科技,', url2)
    read_url()
    save()