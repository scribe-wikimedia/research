import argparse
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import time
# python3 wikidata_information_extractor.py -i wikidata-glam/catalan/bing-all-ca-references.json -o ca-wikidata-criteria.json -l ca


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True,
                help='search results file')
    parser.add_argument('--output', '-o', required=True,
                help='json output file')
    parser.add_argument('--lang', '-l', required=True,
                help='language of the Wikipedia')

    args = parser.parse_args()
    return args


def get_domains(infile):
    domains = set()
    reference_data = json.load(open(infile))
    for r in reference_data:
        domains.add(r['publisher_name'])
    return domains

def get_items(domain, lang):
    domain_qid = {}
    domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
    print(domain)
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    SELECT ?item ?itemLabel ?website ?type ?typeLabel ?pol ?polLabel ?twitter
    WHERE 
    {
      ?item wdt:P856 ?website .
      filter( regex(str(?website), "%s" ) ) .
        OPTIONAL {?item wdt:P31 ?type}
        OPTIONAL {?item wdt:P31 ?type}
        OPTIONAL {?item wdt:P1142 ?pol}
        OPTIONAL {?item wdt:P2002 ?twitter}
        SERVICE wikibase:label { bd:serviceParam wikibase:language "%s, en". }
    } LIMIT 10
    """ % (domain, lang)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        if not domain in domain_qid:
            domain_qid[domain] = []
        domain_data = {'qid': result['item']['value'], 'label': result['itemLabel']['value'],'website': result['website']['value']}
        if 'typeLabel' in result:
            domain_data['type'] = result['typeLabel']['value']
        if 'polLabel' in result:
            domain_data['pol'] = result['polLabel']['value']
        if 'twitter' in result:
            domain_data['twitter'] =  result['twitter']['value']
        print(domain_data)
        domain_qid[domain].append(domain_data)
    return domain_qid

def get_wikidata(domains, lang):
    data = {}
    wait_counter = 0
    for domain in domains:
        data[domain] = get_items(domain, lang)
        wait_counter += 1
        if wait_counter == 10:
            time.sleep(600)
            wait_counter = 0
    return data

def write_to_file(output, data):
    with open(output, 'w') as outfile:
        json.dump(data, outfile)

def main(args):
    domains = get_domains(args.input)
    data = get_wikidata(domains, args.lang)
    write_to_file(data, args.output)


if __name__ == '__main__':
    args = get_args()
    main(args)
