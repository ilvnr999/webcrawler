import requests
from bs4 import BeautifulSoup
import csv
import argparse

def fetch(url):

    output = {"Source_id":None, "Title":None, "Time":None, "Author":None, "Content":None, "Other_picture":None}
    # 取得source_id
    url_split = str(url).split('/')
    url_id = url_split[-2]+url_split[-1].split('?')[0]
    output['Source_id'] = url_id

    responde = requests.get(url)
    html_content = responde.text
    soup = BeautifulSoup(html_content, 'html5lib')

    # 抓取標題
    title = soup.find('h1')
    output['Title'] = title.get_text()

    #抓取時間
    time = soup.find('time')
    output['Time'] = time.get_text()

    #抓取作者
    author = soup.find('div',class_='article-body__info')
    output['Author'] = author.get_text().strip()

    #刪除延伸閱讀
    decompose = soup.find('b',string='延伸閱讀')
    if decompose:
        for element in decompose.find_all_next():
            element.decompose()  # 刪除該標籤及其所有後代
        decompose.decompose()   # 刪除延伸閱讀

    #抓取文章頭的照片與文字
    picture = soup.find('img')
    src = picture.get('src')
    figcaption = soup.find('figcaption')
    if figcaption:
        figcaption_text = figcaption.get_text() + '\n'
    else :
        figcaption_text = ''

    #抓取內容
    content = soup.find('section',class_='article-body__editor')
    for style in content.find_all('style'):
        style.decompose()
    cleaned_text = content.get_text(separator='\n', strip=True)
    cleaned_text = ' '.join(cleaned_text.split())
    output['Content'] = src + figcaption_text + cleaned_text  #文章頭的圖片與照片加入content
    
    #抓取內文中的照片
    img_tags = content.find_all('img')
    image_urls = []
    for img in img_tags:
        src = img.get('src')
        image_urls.append(src)
    if image_urls :output['Other_picture'] = image_urls    
    
        
    #print(image_urls)

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
    # 設定命令行參數解析器
    parser = argparse.ArgumentParser(description='抓取網頁內容，直接將URL貼執行檔在後面')
    parser.add_argument('url', type=str, help='要抓取的網頁 URL')
    # 解析命令行參數
    args = parser.parse_args()

    fetch(args.url)