import os
from collections import Counter

import pandas as pd
import tiktoken
from openai import OpenAI

client = OpenAI()

def read_csv(path):
    df = pd.read_csv(path)
    content = df["content"]
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
        current_batch += content.replace("\n", "") + "\n"
        current_token += content_token
    if current_batch:
        batch_list.append(current_batch.strip())
    return batch_list


def extract_tech_terms(content, model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": prompt},
            {"role": "user", "content":f"Here are some articles separated by ' ':{content}"}
        ],
        temperature=0,
        top_p=1,
        seed=2
    )
    usage = response.usage  # 獲取 usage 欄位
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens
    return response.choices[0].message.content.strip(), prompt_tokens, completion_tokens, total_tokens

def save_csv(path, terms):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        mode = 'w'
    else: 
        mode = 'a'
    terms = dict(Counter(terms))
    print(terms)
    df = pd.DataFrame(list(terms.items()), columns=['名詞', '數量'],index=False)
    df.to_csv(path, mode=mode)

def main():
    model = "gpt-4o"
    prompt = "You are a model that extracts all proper nouns, technical terms, and other nouns that have different expressions in Simplified and \
            Traditional Chinese. The input consists of multiple articles separated by the delimiter ' '. Please ensure that you accurately extract \
            terms from each article, recognizing this delimiter as the boundary between different articles. For example, for ‘Nvidia’, you should \
            return ‘英偉達’ and ‘輝達’. Additionally, include terms like ‘製程’ and ‘工藝’, or ‘雲端運算’ and ‘雲計算’.\
            After extracting the terms, translate based on the context:\
            - If the term is in English, translate it into Traditional Chinese and Simplified Chinese.\
            - If the term is in Traditional Chinese, translate it into English and Simplified Chinese.\
            - If the term is in Simplified Chinese, translate it into English and Traditional Chinese.\
            The output format should be:\
            English: Traditional Chinese: Simplified Chinese\
            Different proper nouns should still be separated by commas."
    max_token = 8000
    read_path = 'tech_news/technews-08_1.csv'
    save_path = 'tech_news/terms_translate.csv'
    terms_list = []
    contents = read_csv(read_path)
    print(contents.str.len().sum())
    batch_list = batch(model, max_token, contents, prompt)
    print(sum(len(batch) for batch in batch_list))
    for cont in batch_list:
        terms_str, prom_token, re_token, tot_token = extract_tech_terms(cont, model, prompt)
        print(prom_token, re_token, tot_token)
        terms = [s.strip() for s in terms_str.split(",")]
        print(terms)
        terms_list.extend(terms)
    save_csv(save_path, terms_list)

if __name__ == "__main__":
    main()
