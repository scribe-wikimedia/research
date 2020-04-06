
import argparse 
import pandas as pd 
import requests 
import json 
from urllib.parse import urlparse

# def main(args):

def get_references(qid, kw, key, lang):
    
    r = bing_search(kw, key, lang)
    
    if r is None: # bing search failed
        return None
    
    d = json.loads(r.text)
    out = []
    if "webPages" not in d:
        return None
        
    for rank, l in enumerate(d["webPages"]["value"]):
        if l["language"] != lang:
            continue
            
        try:
            publisher_name = urlparse(l["url"]).netloc 
        except:
            publisher_name = None

        x = {
        "publisher_name":publisher_name, 
        "publication_title":l["name"], 
        "summary":l["snippet"], 
        "url": l['url'], 
        "quality": round(1/(rank+1),2),   # for sorting 1/rank 
        "publication_date":l["dateLastCrawled"], 
        "retrieved_date":None,
        "content_selection_method":"bing-search",
        "wd_q_id":qid
        }
        out.append(x)
    return out


def bing_search(kw, key, lang):

    try:
        url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
        payload = {'q': kw, 'setLang': lang, 'safesearch': "Strict", "count":100}
        headers = {'Ocp-Apim-Subscription-Key': key}
        r = requests.get(url, params=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    return  r 


if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', '-k', required=True,
                help='key for google search engine api')  
    parser.add_argument('--lang', '-l', required=True,
                help='language of the market of search e.g. ar, ca')      
    parser.add_argument('--input', '-i', required=True,
                help='csv file of no-wikipedia arcitles')
    parser.add_argument('--output', '-o', required=True,
                help='json output file')

    args = parser.parse_args()
    df = pd.read_csv(args.input,sep="\t")
    references = [] 
    for c, row in list(df.iterrows()):
        print("getting refernces for article {}".format(c))
        qid = row["item"].split("/")[-1]
        kw = "\"" + row["label"] + "\""  # exact match
        r = get_references(qid, kw, args.key, args.lang)
        if r is not None:
            references.append([i for i in r])

    # flatten references 
    references = [j for i in references for j in i]
    json.dump(references, open(args.output,"w"))
