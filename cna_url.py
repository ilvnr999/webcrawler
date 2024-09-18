import requests 
from bs4 import BeautifulSoup
from base64 import b64decode
import dateutil.parser
import dateutil.tz
import re

def fetch(url):
    print(url)
    # url = 'https://www.cna.com.tw/news/ait/202409120182.aspx'
    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=("{apikey}", ""),
        json={
            "url": url,
            "httpResponseBody": True,
        },
    )
    if api_response.status_code != 200:
            print(f"Error: Received status code {api_response.status_code}")
            return
    else:
         print(api_response.status_code)

    http_response_body: bytes = b64decode(
        api_response.json()["httpResponseBody"])

    # responde = requests.get(url)    # 返回一個Response物件 通過此物件響應內容狀態碼標頭等訊息
    # html_content = responde.text    # 返回響應內容的字串型態
    responde = http_response_body.decode("utf-8")   # 將解碼後的二進制數據轉換為字符串（假設是 UTF-8 編碼）
    soup = BeautifulSoup(responde, 'html5lib')      # 透過解析器建立BeautifulSoup物件

    # 取得ID
    url_split = str(url).split('/')
    url_num = url_split[-1].split('.')
    source_id = url_split[-2] + '/' + url_num[0]
    # 中央社404狀態200
    if '404' in soup.find('title').text:
         return print('404')
    
    # 抓取標題
    title = soup.find('h1').text

    # 抓取時間
    time = soup.find('div',class_='updatetime')
    if not time :
        time = soup.find('p',class_='article-time')
    
    time = time.get_text()  
    if '（' in str(time):
        time = time.split('（')[0]
    time_plus = str(time) + '+08:00'
    time_turn = dateutil.parser.parse(time_plus).astimezone(dateutil.tz.UTC)

    # 抓取內文
    text = soup.find('div', class_='paragraph')  # 抓取文章區域
    all_p = text.find_all('p')
    p_list = [p.get_text() for p in all_p]
    content = ' '.join(p_list)

    # 抓取文章頭
    picture = soup.find('figure',class_='floatImg center')
    if picture :
        get_picture = picture.find('img')
        img = get_picture.get('src')
        word = get_picture.get('alt')
        content = img + word + content

    other_picture = []
    # 抓取其他照片
    media = soup.find_all('div', class_='media')
    if media:
        for me in media:
            img = me.find('img')
            if img :
                img_img = img.get('data-src')
                img_word = img.get('alt')
                other_picture.append(img_img+img_word)

# 抓取作者
    pattern1 = r'[（(](.*?)[）)]'  # 匹配括號中的內容
    find_author = str(re.findall(pattern1,p_list[0])) + str(re.findall(pattern1,p_list[-1]))
    pattern = r'(記者|編輯|譯者|核稿)[：:]?\s*([\u4e00-\u9fa5]{2,3})'
    matches = re.findall(pattern, find_author)
    # 只提取職位和人名
    author = [' '.join(match) for match in matches]


    return {"source_id":source_id,
            "title":title,
            "time":time_turn,
            "author":author,
            "content":content,
            "other_picture":other_picture}


if __name__ == '__main__':
    url = 'https://www.cna.com.tw/news/afe/202409170209.aspx'
    print(fetch(url))