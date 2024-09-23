import requests
from bs4 import BeautifulSoup

output = {"Title":None, "Time":None, "Author":None, "Content":None, "other_picture":None}
url = 'https://money.udn.com/money/story/5599/8211575?from=edn_maintab_index'

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
figcaption_text = figcaption.get_text() + '\n'



#抓取內容
content = soup.find('section',class_='article-body__editor')
output['Content'] = src + figcaption_text + content.get_text().strip()  

img_tags = content.find_all('img')
image_urls = []
for img in img_tags:
    src = img.get('src')
    image_urls.append(src)
print(image_urls)
'''#寫入csv檔案
fn = url[-10:]+'.csv'
with open(fn, 'w') as file_obj:
    writer = csv.writer(file_obj)
    for key, value in output.items():
        writer.writerow([key,value])
print(output)'''