# get section titles 
import pandas as pd 
import argparse
import os 
import requests 
import numpy as np 
from collections import defaultdict
    

     
    
def get_sections(qid, lang):
    wiki = "{}wiki".format(lang)
    query1= "https://www.wikidata.org/w/api.php?".format(qid, wiki)
    params1 = {"action":"wbgetentities","props":"sitelinks","ids":qid,"sitefilter":wiki, "format":"json"}
    r = requests.get(url = query1, params = params1)
    response = r.json()
    title = response["entities"][qid]["sitelinks"][wiki]["title"]
    
    query2= "https://{}.wikipedia.org/w/api.php?action=parse&page={}&format=json&prop=sections".format(lang, title)
    r = requests.get(url = query2)
    response = r.json()
    return [i for i in response["parse"]["sections"] if i ["toclevel"] == 1]
    

if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True,
                help='tsv file containing wikidata items to \
                    translate their labels')    
    parser.add_argument('--output', '-o', required=True,
                help='output tsv file to add the labels to')    
    parser.add_argument('--lang', default="ar",
                help='lang code of the target wiki ar, ca ..etc')
    parser.add_argument("--sections-per-position", type=int, default=2,
                        help="number of shown sections per position")
    
    args = parser.parse_args()

    x = pd.read_csv(args.input, sep="\t")
    x["item"] = x.apply(lambda i: os.path.basename(i["item"]), axis=1)
    
    # retrieving sections for each wikipedia page
    sections = []
    for c, i in enumerate(x["item"].values):
        try:
            s = get_sections(i, args.lang)
            sections.append(s)
            print("{} of {} : {} sections retrieved".format(c,len(x["item"].values), len(s)))
        except:
            print("qid: {} failed to retrieve sections".format(i))
    
    # create a negative list of all last 3 sections to remove usually they are external links, references 
    negative_list = set([j["line"] for i in sections for j in i[-2:]])
    # removing last 2 auomatically generated sections: external links, references
    sections = [i for i in sections if len(i) > 2]   
    # median # of sections without the last 2  
    average_number_of_sections = np.median([len(i) for i in sections])
    all_sections = [j for i in sections for j in i if j["line"] not in negative_list]
    
    sections_dict = defaultdict(lambda : {"count":0, "positions":[]})                    
    for i in all_sections:
        sections_dict[i["line"]]["count"] +=1
        sections_dict[i["line"]]["positions"].append(int(i["index"]))

    d = [{"section":k, "count":v["count"], "average_position":np.median(v["positions"])} for k,v in sections_dict.items()]
    
    df = pd.DataFrame(d)        
    df["agg_position"] = df.apply(lambda a: int(round(a["average_position"])), axis=1)
    
    template = []
    for i in range(0, int(average_number_of_sections)):
        v = df[df["agg_position"] == i+1].sort_values("count", ascending=False)
        for j in range(0, min(args.sections_per_position, len(v))):
            template.append({"section":v.iloc[j]["section"], "order":i, "rank":j+1})
     
    template = pd.DataFrame(template)
    template.to_csv(args.output, sep="\t", index=False)
    