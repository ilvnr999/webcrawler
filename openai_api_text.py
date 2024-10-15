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
        current_batch += content.replace("\n", "")
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
            {"role": "user", "content":f"Here are some articles:{content}"}
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

def split_terms(terms_str):
    terms_raw = terms_str.split(",")
    terms = []
    error = []
    for s in terms_raw:
        cleaned_s = s.strip()
        split_terms = cleaned_s.split(':')
        if len(terms) <= 3:
            terms.append(split_terms)
        else :
            terms.append(error)    
    return terms, error

def save_csv(path, terms):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        mode = 'w'
        df = pd.DataFrame(terms, columns=['英文', '繁中', '簡中'])
    else: 
        mode = 'a'
    #terms = dict(Counter(terms))
    #print(terms)
    #df = pd.DataFrame(list(terms.items()), columns=['名詞', '數量'],)
        df = pd.DataFrame(terms)
    df.to_csv(path, mode=mode, index=False)

def main():
    model = "gpt-4o"
    prompt = "You are a model that extracts all proper nouns, technical terms, and other nouns that have different expressions in Simplified and \
            Traditional Chinese. The input consists of multiple articles. Please ensure that you accurately extract \
            terms from each article, recognizing this delimiter as the boundary between different articles. For example, for ‘Nvidia’, you should \
            return ‘英偉達’ and ‘輝達’. Additionally, include terms like ‘製程’ and ‘工藝’, or ‘雲端運算’ and ‘雲計算’.\
            After extracting the terms, translate based on the context:\
            - If the term is in English, translate it into Traditional Chinese and Simplified Chinese.\
            - If the term is in Traditional Chinese, translate it into English and Simplified Chinese.\
            - If the term is in Simplified Chinese, translate it into English and Traditional Chinese.\
            The output should format each term by first providing the English term, followed by a colon, \
            then the Traditional Chinese term with another colon, and finally the Simplified Chinese term. \
            The output should be formatted as follows: Each term should be presented in the format \
            'English: Traditional Chinese: Simplified Chinese'. Please ensure there are no numbers or additional text in the output. Different \
            proper nouns should be separated by commas, and between each pair of commas, there should only be two colons separating the three terms."
    max_token = 8000
    read_path = 'tech_news/technews-08_2.csv'
    save_path = 'tech_news/terms_translate3.csv'
    terms_list = []
    contents = read_csv(read_path)
    print(contents.str.len().sum())
    batch_list = batch(model, max_token, contents, prompt)
    print(sum(len(batch) for batch in batch_list))
    for cont in batch_list:
        terms_str, prom_token, re_token, tot_token = extract_tech_terms(cont, model, prompt)
        print(prom_token, re_token, tot_token)
        print("terms_str:\n", terms_str)
        terms, error = split_terms(terms_str)
        print("terms after split:\n",terms)
        print("more than three elements:\n")
        terms_list.extend(terms)
    save_csv(save_path, terms_list)

if __name__ == "__main__":
    main()
