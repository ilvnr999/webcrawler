import os
from collections import Counter

import pandas as pd
import tiktoken
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class TermsStructure(BaseModel):
    proper_nuons : list[str]

def read_csv(path):
    df = pd.read_csv(path)
    content = df["Content"]
    return content 

def batch(model, max_token, content_list, prompt):
    enc = tiktoken.encoding_for_model(model)
    batch_list = []
    estimated_prompt_token = len(enc.encode(prompt))  # 计算系统提示的令牌数
    current_batch = ""
    current_token = estimated_prompt_token
    for content in content_list:
        content_token = len(enc.encode(content))
        if current_token + content_token > max_token:
            batch_list.append(current_batch)
            current_batch = ""
            current_token = estimated_prompt_token
        current_batch += content.strip() + "\n***\n"
        current_token += content_token
    if current_batch:
        batch_list.append(current_batch.strip())
    return batch_list


def extract_tech_terms(content, model, prompt):
    complition = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system",
             "content": prompt},
            {"role": "user", "content":f"Here are some articles separated by '***':{content}"}
        ],
        temperature=0,
        top_p=1,
        seed=2,
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
    terms = dict(Counter(terms))
    print(terms)
    df = pd.DataFrame(list(terms.items()), columns=['名詞', '數量'])
    df.to_csv(path, mode=mode)

def main():
    model = "gpt-4o"
    prompt = "You are a model that extracts all proper nouns, technical terms, and other nouns that have different expressions in \
                    Simplified and Traditional Chinese. The input consists of multiple articles separated by the delimiter '***'. Please ensure that \
                    you accurately extract terms from each article, recognizing this delimiter as the boundary between different articles. \
                    For example, for 'Nvidia', you should return '英伟达' and '輝達'. Additionally, include terms like '製程' and '工艺', \
                    or '雲端運算' and '雲計算'. Focus on capturing brand names, company names, product names, and any other relevant terms, \
                    returning only the extracted terms without any additional explanation."
    max_token = 8000
    read_path = 'csv/line_api.csv'
    save_path = 'csv/terms6_4o.csv'
    terms_list = []
    contents = read_csv(read_path)
    print(contents.str.len().sum())
    batch_list = batch(model, max_token, contents, prompt)
    print(sum(len(batch) for batch in batch_list))
    for cont in batch_list:
        terms_str = extract_tech_terms(cont, model, prompt)
        terms = terms_str.proper_nuons
        print(terms)
        terms_list.extend(terms)
    save_csv(save_path, terms_list)

if __name__ == "__main__":
    main()
