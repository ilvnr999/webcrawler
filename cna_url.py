import aiohttp
import asyncio
import base64
from bs4 import BeautifulSoup
import dateutil.parser
import dateutil.tz
import re

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        # 使用 BasicAuth 對象來提供認證資訊
        auth = aiohttp.BasicAuth('5c532da8add642e6bf662951b506adac', '')
        async with session.post(
            "https://api.zyte.com/v1/extract",
            auth=auth,
            json={"url": url, "httpResponseBody": True}
        ) as response:
            if response.status != 200:
                print(f"Error: Received status code {response.status}")
                return

            response_json = await response.json()
            http_response_body = base64.b64decode(response_json["httpResponseBody"])

    html = http_response_body.decode("utf-8")
    soup = BeautifulSoup(html, 'html5lib')

    # 取得ID
    url_split = str(url).split('/')
    url_num = url_split[-1].split('.')
    source_id = url_split[-2] + '/' + url_num[0]
    
    # 中央社404狀態200
    if '404' in soup.find('title').text:
        print('404')
        return {"status": "error", "message": "404 not found"}

    # 抓取類別
    categories = soup.find('a', class_='blue')
    if categories:
        categories = categories.get_text()

    # 抓取標題
    title = soup.find('h1').text

    # 抓取時間
    time = soup.find('div', class_='updatetime')
    if not time:
        time = soup.find('p', class_='article-time')
    
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
    picture = soup.find('figure', class_='floatImg center')
    if picture:
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
            if img:
                img_img = img.get('data-src')
                img_word = img.get('alt')
                other_picture.append(img_img + img_word)

    # 抓取作者
    pattern1 = r'[（(](.*?)[）)]'  # 匹配括號中的內容
    find_author = str(re.findall(pattern1, p_list[0])) + str(re.findall(pattern1, p_list[-1]))
    for i in range(-2, len(p_list) if len(p_list) < 4 else -5 , -1):
        find_author += str(re.findall(pattern1, p_list[i]))
    pattern = r'(記者|編輯|譯者|核稿)[：:]?\s*([\u4e00-\u9fa5]{2,3})'
    matches = re.findall(pattern, find_author)
    author = ''.join(f"{work}{name}" for work, name in matches)
    print(author)
    
    if not author:
        author = 'none'
    if not categories:
        categories = 'none'
    

    return {
        "source_id": source_id,
        "title": title,
        "time": time_turn,
        "author": author,
        "content": content,
        "other_picture": other_picture,
        "categories": categories
    }

# 用於測試異步 fetch 函數的示例代碼
async def main():
    url = 'https://www.cna.com.tw/news/aopl/202409190010.aspx'
    result = await fetch(url)
    #print(result)

if __name__ == '__main__':
    asyncio.run(main())
