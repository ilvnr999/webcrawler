import csv

import feedparser

from ltn_url import fetch


def grab():
    # 指定RSS feed的URL
    rss_url = 'https://news.ltn.com.tw/rss/business.xml'

    # 解析RSS feed
    feed = feedparser.parse(rss_url)
    url_list = []
    url_content = []
    fieldnames = []
    # 遍歷所有的條目，提取並打印URL
    for entry in feed.entries:
        #fetch(entry)
        #print(entry.link)
        url_list.append(entry.link)
    #print('rss中的url',str(url_list))
    
    # 讀取內容
    for url in url_list:
        content = fetch(url)
        if content ==  0:
            continue
        url_content.append(content)
    # 讀取行名稱
    first_dict = url_content[0]
    for key in first_dict:
        fieldnames.append(key)
    print('column names',fieldnames)

    csv_name = 'ltn.csv'
    with open(csv_name, 'w', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in url_content:
            writer.writerow(row)

if __name__ == '__main__':
    grab()