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
              "categories" : None, 
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

    # 讀取categories

    categories = soup.find_all('a', class_ = 'breadcrumb-items')
    if len(categories) < 2:
        print('非udn')
        return 0
    else:
        categories = categories[1].get_text()
    if categories != '產經': 
        print('非產經類',categories)
        return 0
    output['categories'] = categories

    # 抓取標題
    title = soup.find('h1')
    output['Title'] = title.get_text()

    #抓取時間
    time = soup.find('time').text
    time_plus = str(time) + '+08:00'
    time_turn = dateutil.parser.parse(time_plus).astimezone(dateutil.tz.UTC)
    output['Time'] = str(time_turn)
    
    #抓取作者
    author_info = soup.find('span',class_='article-content__author')
    author = author_info.find('a')
    if author:
        author = author.get_text().strip()
    else:
        author = author_info.get_text()
        if '/' in author:
            author = author.split('/')[0]
        if '／' in author:
            author = author.split('／')[0]
    output['Author'] = author
    
    #print(output)

    #抓取文章頭的照片與文字
    picture = soup.find('figure', class_ = 'article-content__cover')
    if picture:
        src = picture.find('img').get('src')
        figcaption = picture.find('figcaption').text
    else:
        src = ''
        figcaption = ''


    #抓取內容
    text = soup.find('section', class_='article-content__editor')  # 抓取文章區域
    all_p = text.find_all('p', style=None)
    p_list = [p.get_text().strip() for p in all_p]
    content = ' '.join(p_list)
    output['Content'] = src + figcaption + content  #文章頭的圖片與照片加入content
    
    #抓取內文中的照片
    img_tags = text.find_all('img')
    image_urls = []
    if img_tags:
        for img in img_tags:
            src = img.get('src')
            image_urls.append(src)
            output['Other_picture'] = image_urls    
    
        
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
    url = 'https://ec.ltn.com.tw/article/breakingnews/4808252'
    fetch(url)