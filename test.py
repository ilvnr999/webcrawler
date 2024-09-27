import time

from bs4 import BeautifulSoup
from selenium import webdriver

from line_url import fetch

url = 'https://today.line.me/tw/v3/page/finance'
# 設定 WebDriver
driver = webdriver.Chrome()  # 確保你已經安裝了 ChromeDriver
driver.get(url)
# 模擬滾動到頁面底部
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 等待頁面加載
time.sleep(2)  # 可以根據需要調整這個時間

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

target_divs = soup.find_all('div', attrs={'data-anchor-id': True})

# 遍歷每個 <div>，並查找其內部的 <h2>
for div in target_divs:
    h2_tag = div.find('h2')  # 查找內部的 <h2>
    if h2_tag:
        h2 = '理財' + h2_tag.text.strip()
        '''if "財知道" in h2 :
            continue'''
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
                print(fetch(url, h2))


















'''top = soup.find('div', {'data-anchor-id': "66ac67576bf9c1541d469ee1"})
cate = top.find('h2')
print(cate.text)
urls = top.find_all('a', class_='ltcp-link')
for url in urls:
    print(url.get('href'))'''
'''# 查找需要的內容
h2 = soup.find_all('h2')
print([element.get_text() for element in h2])
categories = soup.find_all('a', class_='ltcp-link')
links = [link.get('href') for link in categories]

# 打印所有的連結
for link in links:
    if '/tw/v2/article/' in str(link):
        str1 = 'https://today.line.me' + link
        print(fetch(str1))
'''
#print(categories)

driver.quit()