import feedparser
from money_udn_url import fetch
import csv
import argparse

def grab(csv_name, rss_url):
    # 指定RSS feed的URL
    #rss_url = 'https://money.udn.com/rssfeed/news/1001/5591/5612?ch-=money'

    # 解析RSS feed
    feed = feedparser.parse(rss_url)
    url_list = []
    url_content = []
    fieldnames = []
    # 遍歷所有的條目，提取並打印URL
    for entry in feed.entries:
        #fetch(entry)
        print(entry.link)
        url_list.append(entry.link)
    print('rss中的url',str(url_list))
    
    # 讀取內容
    for url in url_list:
        url_content.append(fetch(url))
    # 讀取行名稱
    first_dict = url_content[0]
    for key in first_dict:
        fieldnames.append(key)
    print('column names',fieldnames)

    with open(csv_name, 'a', encoding='utf-8', newline='') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in url_content:
            writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='抓取rss網頁內容')
    #添加兩個參數
    parser.add_argument('csv_name', type=str, help='要存入的csv名稱')
    parser.add_argument('rss', type=str, help='要抓取的rss')
    # 調用函數
    args = parser.parse_args()

    grab(args.csv_name, args.rss)
    print('Done!')