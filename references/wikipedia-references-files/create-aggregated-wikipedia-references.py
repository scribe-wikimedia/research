import jsonlines
from urllib.parse import urlsplit
import json


def get_base_url(url):
    try:
        netloc = urlsplit(url).netloc
        if netloc.startswith("www."):
            netloc = netloc.replace("www.","")
        return netloc if len(netloc) > 0 else None
    except:
        print("cannot get base url for {}".format(url))
        return None


def count_domains(input):
    domains = {}
    with jsonlines.open(input) as infile:
        for obj in infile:
            for ref in obj['references']:
                if not isinstance(ref, dict) or 'url' not in ref:
                    continue
                domain = get_base_url(ref['url'])
                if domain not in domains:
                    domains[domain] = 1
                    print(domain)
                else:
                    domains[domain] += 1
    return domains


json.dump(count_domains('ca.references.ljson'), open('ca.references.aggregated.json','w'))
json.dump(count_domains('ar.references.ljson'), open('ar.references.aggregated.json','w'))