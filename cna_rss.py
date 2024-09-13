import feedparser
from cna_url import fetch

def grab():
    url1 = 'https://feeds.feedburner.com/rsscna/technology'
    url2 =  'https://feeds.feedburner.com/rsscna/finance'
    feed1 = feedparser.parse(url1)
    feed2 = feedparser.parse(url2)
    url_list = []
    field_name = []

    for entry in feed1.entries:
        url_list.append(entry.link)
    for entry in feed2.entries:
        url_list.append(entry.link)
    # print(url_list)
    # 讀取url
    for url in tuple(url_list):
        print(fetch(url))
    
if __name__ == '__main__':
    grab()