import re
from base64 import b64decode
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


def remove_keyword(text, keywords):
    '''將文章末 各家新聞的廣告刪除'''
    for keyword in keywords:
        if keyword in text:
            text = text.split(keyword)[0]
    return text

def fetch(url, categories=None):
    '''抓取url上的標題、時間、作者、內文與其他照片'''
    print(url)
    output = {"Source_id" : None, 
              "Title" : None, 
              "Time" : None, 
              "Author" : None, 
              "Content" : None,
              "Categories" : categories, 
              "Other_picture" : []}
    
    # 取得source_id
    url_split = str(url).split('/')
    output['Source_id'] = url_split[-1]

    api_response = requests.post(
    "https://api.zyte.com/v1/extract",
    auth=("bbc1a2b309d74e21a8cc452e054e54d5", ""),
    json={
        "url": url,
        "httpResponseBody": True,
    },
    )
    http_response_body: bytes = b64decode(api_response.json()["httpResponseBody"])

    soup = BeautifulSoup(http_response_body, 'html5lib')  # 解析成HTML樹狀結構

    if soup.find('figure', class_ = 'entityVideoPlayer-wrapper'):
        print('video')
        return 0

    '''# 讀取categories
    categories_block = soup.find('div', class_ = 'breadcrumbs boxTitle')
    categories_list= categories_block.find_all('a')
    categories = [a.get_text() for a in categories_list]
    output['Categories'] = categories'''

    # 抓取標題
    title = soup.find('h1')
    title_strip = title.get_text().replace('\u3000', ' ').strip()
    output['Title'] = title_strip

    #抓取文章頭的照片與文字
    picture = soup.find('div', class_ = 'image-wrapper image-wrapper-withsizes')
    if picture:
        img = picture.find('img').get('src')
    else:
        img = ''

    article = soup.find('article', class_='news-content textSize--md')
    # 刪除不必要內容
    ul = article.find('ul')
    if ul:
        for element in ul.find_all_next():
            element.decompose()  # 刪除該標籤及其所有後代
            ul.decompose()   # 刪除延伸閱讀
    #print(article.get_text())
    
    # 抓取內容
    keywords = ['延伸閱讀', '＊編者按：','下載「財訊快報App」最即時最專業最深度','立刻加入','《民視新聞網》提醒您', '更多']
    content = article.find_all_next(['p','h3'], herf=False)
    text = [element.get_text() for element in content]
    text = ''.join(text)
    remove_keyword(text, keywords)
    output['Content'] = str(img)  + str(text)  #文章頭的圖片與照片加入content
    
    # 抓取時間
    div = soup.find('div',class_='entityPublishInfo-meta')
    time = div.find('span')
    '''time_plus = str(time) + '+08:00'
    time_turn = dateutil.parser.parse(time_plus).astimezone(dateutil.tz.UTC)'''
    time = str(time.get_text().strip()).split(' • ')
    
    
    if len(time) >= 3:
        author2 = time[2]
    else:
        author2 = ""
    pattern = r"發布於"
    for t in time: 
        if re.search(pattern, t): 
            ago = t
    current_time = datetime.now()
    if '小時' in ago:
        match = re.search(r'\d+', ago)
        number = int(match.group())
        new_time = current_time - timedelta(hours=number)
    elif '分鐘' in ago:
        match = re.search(r'\d+', ago)
        number = int(match.group())
        new_time = current_time - timedelta(minutes=number)
    else:
        new_time=ago
    output['Time'] = str(new_time)


    # 抓取作者
    
    author = div.find('a').text.strip()
    output['Author'] = author + author2

    #抓取內文中的照片
    img_tags = article.find_all_next('img')
    if img_tags :
        image_urls= [img.get('src') for img in img_tags[1:] if img.get('src') != '']
        output['Other_picture'] = image_urls

    #寫入csv檔案
    ''' fieldnames = list(output.keys())
    print(fieldnames)
    with open('all_url.csv', 'a', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(output)'''
    print(output)
    
    return output

if __name__ == '__main__':
    url = 'https://today.line.me/tw/v2/article/rmnMEg0'
    fetch(url)