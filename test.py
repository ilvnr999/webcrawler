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
time.sleep(3)  # 可以根據需要調整這個時間

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# 查找需要的內容
categories = soup.find_all('a', class_='ltcp-link')
links = [link.get('href') for link in categories]

# 打印所有的連結
for link in links:
    if '/tw/v2/article/' in str(link):
        str1 = 'https://today.line.me' + link
        print(fetch(str1))

#print(categories)

driver.quit()