import requests
from bs4 import BeautifulSoup
import csv
import argparse
import asyncio
import dateutil.parser
import dateutil.tz

def fetch(url):

    output = {"Source_id":None, "Title":None, "Time":None, "Author":None, "Content":None, "Other_picture":None}
    # 取得source_id
    url_split = str(url).split('/')
    url_id = url_split[-2]+url_split[-1].split('?')[0]
    output['Source_id'] = url_id

    responde = requests.get(url)
    html_content = responde.text
    soup = BeautifulSoup(html_content, 'html5lib')
    article = soup.find('article')


    #抓取時間
    '''time = soup.find('time')
    output['Time'] = time.get_text()'''

    p_text = article.find('p').text
    l = p_text.split(' ')
    author = l[0]
    created_str = l[-2] + ' ' + l[-1] + '+08:00'
    created = dateutil.parser.parse(created_str).astimezone(dateutil.tz.UTC)
    
    return print({'created':created})

if __name__ == '__main__':
    # 設定命令行參數解析器
    parser = argparse.ArgumentParser(description='抓取網頁內容，直接將URL貼執行檔在後面')
    parser.add_argument('url', type=str, help='要抓取的網頁 URL')
    # 解析命令行參數
    args = parser.parse_args()

    fetch(args.url)