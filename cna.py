from base64 import b64decode

import requests

api_response = requests.post(
    "https://api.zyte.com/v1/extract",
    auth=("bbc1a2b309d74e21a8cc452e054e54d5", ""),
    json={
        "url": "https://feeds.feedburner.com/rsscna/technology",
        "httpResponseBody": True,
    },
)
http_response_body: bytes = b64decode(
    api_response.json()["httpResponseBody"])
# 將解碼後的二進制數據轉換為字符串（假設是 UTF-8 編碼）
decoded_content = http_response_body.decode("utf-8")

# 打印解碼後的內容
print(decoded_content)