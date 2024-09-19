import asyncio
import feedparser
from cna_url import fetch

async def grab():
    url1 = 'https://feeds.feedburner.com/rsscna/technology'
    url2 =  'https://feeds.feedburner.com/rsscna/finance'
    feed1 = feedparser.parse(url1)
    feed2 = feedparser.parse(url2)
    url_list = set()

    for entry in feed1.entries:
        url_list.add(entry.link)
    for entry in feed2.entries:
        url_list.add(entry.link)

    # 使用 asyncio.gather 來並行調用 fetch 函數
    fetch_tasks = [fetch(url) for url in url_list]
    results = await asyncio.gather(*fetch_tasks)

    '''for result in results:
        print(result) ''' # 顯示結果

if __name__ == '__main__':
    asyncio.run(grab())
