import requests

url = 'https://www.cna.com.tw/news/ahel/202409150074.aspx'
#response = requests.get(url)
#print(response.status_code)
api_response = requests.post(
    "https://api.zyte.com/v1/extract",
    auth=("bbc1a2b309d74e21a8cc452e054e54d5", ""),
    json={
        "url": url,
        "httpResponseBody": True,
    },
)
status = api_response.status_code
if status != 200:
        print(f"Error: Received status code {api_response.status_code}")
print(status)