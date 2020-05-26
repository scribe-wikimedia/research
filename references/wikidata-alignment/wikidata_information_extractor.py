# Run using this command
# curl https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.bz2 | bzcat | grep "P856" | cut -d" " -f1,3 | sed -e "s/[\<\>]//g" | python wikidata_information_extractor.py > ar_ca_matched_domains.csv


import json 
from tld import get_tld
import sys 

def get_base_url(url):
    try:
        return get_tld(url, as_object=True).fld
    except:
        print("cannot get base url for {}".format(url), file=sys.stderr)
        return None

ar = json.load(open("../wikidata-glam/arabic/bing-all-ar-references.json"))   
ca = json.load(open("../wikidata-glam/catalan/bing-all-ca-references.json"))
#Get base url (domain name ) from each url in the bing retreived list
ar = set([a for a  in [get_base_url(i["url"]) for i in ar] if a is not None]) 
ca = set([a for a  in [get_base_url(i["url"]) for i in ca] if a is not None]) 


if __name__ == '__main__':

    for source in sys.stdin:
        a,b = source.strip().split()
        b = get_base_url(b) 
        if b in ar:
            print("{}\t{}\tar".format(a,b))
        if b in ca:
            print("{}\t{}\tca".format(a,b))
