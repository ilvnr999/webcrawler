import json
from datetime import datetime

import pytz
import requests


def crawl_single_page():
    url = "https://stocknewsapi.com/api/v1/category?section=alltickers&page=2&items=50&token=b89ih10qjlof59my6rnigv108h39d5p4r8fmkmh5"
    response = requests.get(url)
    json_obj = json.loads(response.text)['data']
    for source in json_obj:
        # categories
        source["topics"].insert(0, "alltickers")

        # create
        time_format = "%a, %d %b %Y %H:%M:%S %z"
        local_time = datetime.strptime(source["date"], time_format)  # 將字串解析為 datetime 物件
        created = local_time.astimezone(pytz.utc)  # 轉換為 UTC

        yield {
            "status": "success",
            "tags":source["tickers"],
            "categories": source["topics"],
            "discription":source["text"],
            "division":source["type"].lower(),
            "source_id": source["news_url"],
            "title": source["title"],
            "created": created,
        }

def main():
    a = list(crawl_single_page())
    for i in a:
        print(i["created"])

if __name__ == "__main__":
    main()