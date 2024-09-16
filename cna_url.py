import requests 
from bs4 import BeautifulSoup
from base64 import b64decode
import dateutil.parser
import dateutil.tz

def fetch(url):
    print(url)
    # url = 'https://www.cna.com.tw/news/ait/202409120182.aspx'
    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=("bbc1a2b309d74e21a8cc452e054e54d5", ""),
        json={
            "url": url,
            "httpResponseBody": True,
        },
    )
    if api_response.status_code != 200:
            print(f"Error: Received status code {api_response.status_code}")
            return
    
    http_response_body: bytes = b64decode(
        api_response.json()["httpResponseBody"])

    # responde = requests.get(url)    # 返回一個Response物件 通過此物件響應內容狀態碼標頭等訊息
    # html_content = responde.text    # 返回響應內容的字串型態
    responde = http_response_body.decode("utf-8")   #將解碼後的二進制數據轉換為字符串（假設是 UTF-8 編碼）
    soup = BeautifulSoup(responde, 'html5lib')      #透過解析器建立BeautifulSoup物件

    # 取得ID
    source_id_last = str(url).split('/')[-1]
    source_id = source_id_last.split('.')[0]

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

    # 抓取作者
    author = soup.find('')

    # 抓取內文
    text = soup.find('div', class_='paragraph')  # 抓取文章區域
    all_p = text.find_all('p')
    content = ' '.join([p.get_text() for p in all_p])
         

    return {"source_id":source_id,
            "title":title,
            "time":time_turn,
            "author":author,
            "content":content}


if __name__ == '__main__':
    url = 'https://www.cna.com.tw/news/ait/202409120379.aspx'
    print(fetch(url))