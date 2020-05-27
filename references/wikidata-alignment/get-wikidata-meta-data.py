import json
import jsonlines
import argparse
import requests

# usage:
# python3 get-Wikidata-meta-data.py ar_ca_matched_domains_uniq.csv wikidata-information.json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='search results file')
    parser.add_argument('output', help='json output file')

    args = parser.parse_args()
    return args


def get_input_file_data(input):
    wikidata_ids = {}
    with open(input) as infile:
        for line in infile:
            tmp = line.strip().split('\t')
            if 'http://www.wikidata.org/entity/Q' not in tmp[0]:
                continue
            qid = tmp[0].replace('http://www.wikidata.org/entity/', '')
            url = tmp[1]
            if url not in wikidata_ids:
                wikidata_ids[url] = []
            wikidata_ids[url].append({'qid': qid, 'language': tmp[2]})
    return wikidata_ids


def get_data_from_statements(entity_data):
    # get types
    types = []
    if 'P31' in entity_data['claims']:
        for t in entity_data['claims']['P31']:
            types.append(t['mainsnak']['datavalue']['value']['id'])

    # get twitter and twitter followers
    twitter = {}
    if 'P2002' in entity_data['claims']:
        for t in entity_data['claims']['P2002']:
            username = t['mainsnak']['datavalue']['value']
            twitter[username] = []
            if 'qualifiers' in t and 'P3744' in t['qualifiers']:
                twitter[username] = t['qualifiers']['P3744'][0]['datavalue']['value']['amount']

    # get political alignemt
    political_alignment = []
    if 'P1387' in entity_data['claims']:
        for t in entity_data['claims']['P1387']:
            political_alignment.append(t['mainsnak']['datavalue']['value']['id'])
    if 'P1142' in entity_data['claims']:
        for t in entity_data['claims']['P1142']:
            political_alignment.append(t['mainsnak']['datavalue']['value']['id'])
    return [types, twitter, political_alignment]


def make_request(qid):
    url = 'https://www.wikidata.org/wiki/Special:EntityData/' + qid + '.json'
    text = json.loads(requests.get(url).text)
    entity_data = text['entities'][qid]
    title = ''
    if 'en' in entity_data['labels']:
        title = entity_data['labels']['en']['value']
    types, twitter, political_alignment = get_data_from_statements(entity_data)
    return [title, types, twitter, political_alignment]


def get_meta_data(input):
    domains = {}
    input_data = get_input_file_data(input)
    for url, qid_lists in input_data.items():
        for meta in qid_lists:
            title, types, twitter, political_alignment = make_request(meta['qid'])
            if not url in domains:
                domains[url] = []
            domains[url].append({'qid': meta['qid'], 'ref_lang': meta['language'], 'en_title': title, 'types': types,
                                 'twitter': twitter, 'political_alignment': political_alignment})
            print(url, domains[url])
    return domains


def write_domains(output, domains):
    json.dump(domains, open(output, 'w'))

def main(input, output):
    domains = get_meta_data(input)
    write_domains(output, domains)


if __name__ == '__main__':
    args = get_args()
    main(args.input, args.output)