import requests
from bs4 import BeautifulSoup


def remove_keyword(text, keywords):
    for keyword in keywords:
        if keyword in text:
            text = text.split(keyword)[0]
    return text

def fetch(url):
    '''抓取url上的標題、時間、作者、內文與其他照片'''
    print(url)
    output = {"Source_id" : None, 
              "Title" : None, 
              "Time" : None, 
              "Author" : None, 
              "Content" : None,
              "Categories" : None, 
              "Other_picture" : None}
    
    # 取得source_id
    url_split = str(url).split('/')
    output['Source_id'] = url_split[-1]

    response = requests.get(url)
    if response.status_code != 200:  # 狀態不為200跳出
        return print(f'{url} \n status = {response.status_code}')
    
    # 讀取HTML內文
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html5lib')  # 解析成HTML樹狀結構

    if soup.find('span', class_ = 'error-text'):
        print('404')
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
    img = picture.find('img').get('src')
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
    content = picture.find_all_next(['p','h3'], herf=False)
    text = [element.get_text() for element in content]
    text = ''.join(text)
    remove_keyword(text, keywords)
    output['Content'] = str(img)  + str(text)  #文章頭的圖片與照片加入content
    
    # 抓取作者
    div = soup.find('div',class_='entityPublishInfo-meta')
    author = div.find('a').text.strip()
    output['Author'] = author

    # 抓取時間
    time = div.find('span')
    '''time_plus = str(time) + '+08:00'
    time_turn = dateutil.parser.parse(time_plus).astimezone(dateutil.tz.UTC)'''
    output['Time'] = str(time.get_text().strip())

    #抓取內文中的照片
    img_tags = picture.find_all_next('img')
    if len(img_tags) > 2 :
        image_urls= [img.get('src') for img in img_tags]
        output['Other_picture'] = image_urls

    #寫入csv檔案
    ''' fieldnames = list(output.keys())
    print(fieldnames)
    with open('all_url.csv', 'a', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(output)'''
    #print(output)
    
    return output

if __name__ == '__main__':
    url = 'https://today.line.me/tw/v2/article/wJO17gl'
    fetch(url)