import dateutil.parser
import dateutil.tz
import requests
from bs4 import BeautifulSoup


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

    responde = requests.get(url)
    if responde.status_code != 200:  # 狀態不為200跳出
        return print(f'{url} \n status = {responde.status_code}')
    
    # 讀取HTML內文
    html_content = responde.text
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
    output['Title'] = title.get_text().strip()
    print(output['Title'])

    '''# 抓取時間
    time = soup.find_all('span', class_='entityPublishInfo-meta-info text text--f text--secondary text--regular entityPublishInfo-meta-info--visible')
    print(time)
    time_plus = str(time) + '+08:00'
    time_turn = dateutil.parser.parse(time_plus).astimezone(dateutil.tz.UTC)
    output['Time'] = str(time_turn)'''
    
    #print(output)

    #抓取文章頭的照片與文字
    picture = soup.find('div', class_ = 'image-wrapper image-wrapper-withsizes')
    img = picture.find('img').get('src')
    article = soup.find('article', class_='news-content textSize--md')
 
    # 抓取內容
    ul = article.find('ul')
    for element in ul.find_all_next():
            element.decompose()  # 刪除該標籤及其所有後代
            ul.decompose()   # 刪除延伸閱讀
    #print(article.get_text())
    content = picture.find_all_next()
    output['Content'] = str(img)  + str(content)  #文章頭的圖片與照片加入content
    print(output['Content'])
    #抓取作者
    author = p_list[0]
    print(author)
    if '/' in author:
        author = author.split('/')
    if '／' in author:
        author = author.split('／')
    if '核稿編輯' in author:
        author = author[1] + author[0]
    else:
        author = author[0][1:]
    output['Author'] = author


    '''if author:
        author = author.get_text().strip()
    else:
        author = author_info.get_text()
        if '/' in author:
            author = author.split('/')[0]
        if '／' in author:
            author = author.split('／')[0]
    output['Author'] = author'''

    '''#抓取內文中的照片
    img_tags = text.find_all('img')
    image_urls = []
    if img_tags:
        for img in img_tags:
            src = img.get('src')
            image_urls.append(src)
            output['Other_picture'] = image_urls'''    
    
        
    #print(image_urls)

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
    url = 'https://today.line.me/tw/v2/article/2DO5plP'
    fetch(url)