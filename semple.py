import os

import pandas as pd
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class TermsStructure(BaseModel):
    proper_nuons : list[str]

def read_csv(path):
    df = pd.read_csv(path)
    content = df["Content"]
    return content 

def extract_tech_terms(content):
    complition = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "你是一個專業的科技內容分析師，能夠從文章中提取出科技相關的專有名詞。"},
            {"role": "user", "content": "請從以下文章中提取所有科技、電子、半導體、汽車、以及新興科技等領域的專有名詞。\
             例如:半導體的矽基氮化鎵、先進製程，電池的12V與48V，純電動車，自動駕駛系統、盲點偵測系統，自動緊急煞車系統，3D人臉辨識、影像處理晶片，雲端運算、運算型伺服器，化合物半導體、電流均一性，汽車市場規模、成本結構優化。"},
            {"role": "user", "content":content}
        ],
        response_format=TermsStructure,
    )
    return complition.choices[0].message.parsed

def extract_list(terms_str):
    terms_str = terms_str.split(",", 1)[1].rstrip(')')
    terms_list = eval(terms_str)
    return terms_list

def save_csv(path, terms):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        mode = 'w'
    else: 
        mode = 'a'
    terms = list(set(terms))
    df = pd.DataFrame({"繁中":terms})
    df.to_csv(path, mode=mode)

def main():
    read_path = 'csv/line_api.csv'
    save_path = 'csv/terms3.csv'
    terms_list = []
    contents = read_csv(read_path)
    for cont in contents:
        terms_str = extract_tech_terms(cont)
        terms = terms_str.proper_nuons
        terms_list.extend(terms)
    save_csv(save_path, terms_list)

if __name__ == "__main__":
    main()
