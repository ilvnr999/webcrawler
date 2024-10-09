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
             "content": "You are a helpful assistant specialized in extracting specialized terms from various fields. Your task is to identify and extract specific terminologies. For example, in the context of machine learning, focus on terms like 'machine learning', 'deep learning' 'Python' 'data science' and others. Please pay attention to context to provide the most relevant terms."},
            {"role": "user", "content": content}
        ],
        response_format=TermsStructure,
    )
    return complition.choices[0].message.parsed

def save_csv(path, terms):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        mode = 'w'
    else: 
        mode = 'a'
    df = pd.DataFrame({"繁中":terms})
    df.to_csv(path, mode=mode)

def main():
    read_path = 'csv/line_api.csv'
    save_path = 'csv/terms.csv'
    terms_list = []
    contents = read_csv(read_path)
    for cont in contents:
        terms = extract_tech_terms(cont)
        terms_list.extend(terms)
    save_csv(save_path, terms_list)

if __name__ == "__main__":
    main()
