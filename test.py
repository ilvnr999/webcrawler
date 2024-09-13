import requests

rss = 'https://feeds.feedburner.com/rsscna/technology'
response = requests.get(rss)
print(response.text)