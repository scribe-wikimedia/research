import json
import jsonlines
import argparse
import requests

# usage:
# python3 get-wikidata-meta-data.py ar_ca_matched_domains_uniq.csv wikidata-information.json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='search results file')
    parser.add_argument('output', help='json output file')

    args = parser.parse_args()
    return args


def get_input_file_data(input):
    """ Get data from the input file
    The input file should be a tsv file
    :param input: input file name
    :return: dict in the form {<url>: [{qid: <qid>, language: <language>}], ...}
    """
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
    """ Get the statements we want to look at from a json Wikidata entity
    :param entity_data: data about an entity
    :return: type (P31), twitter username (P2002) including number of subscribers (P3744), and
             political alignment (P1387 or P1142) in a list in this order (each can be multiple values)
    """
    # get types
    types = []
    if 'P31' in entity_data['claims']:
        for t in entity_data['claims']['P31']:
            if not 'mainsnak' in t or not 'datavalue' in t['mainsnak']:
                continue
            types.append(t['mainsnak']['datavalue']['value']['id'])

    # get twitter and twitter followers
    twitter = {}
    if 'P2002' in entity_data['claims']:
        for t in entity_data['claims']['P2002']:
            if not 'mainsnak' in t or not 'datavalue' in  t['mainsnak']:
                continue
            username = t['mainsnak']['datavalue']['value']
            twitter[username] = []
            if 'qualifiers' in t and 'P3744' in t['qualifiers']:
                if not 'mainsnak' in t or not 'datavalue' in t['mainsnak']:
                    continue
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
    """ Given a Wikidata id, make a request to the Special:EntityData interface on Wikidata
    :param qid: Q-id for a Wikidata item
    :return: for the qid, get the title in English, type,
             twitter username (including number of followers) and political alignment
    """
    url = 'https://www.wikidata.org/wiki/Special:EntityData/' + qid + '.json'
    text = requests.get(url).text
    print(text)
    if not text:
        return None
    try:
        text = json.loads(text)
    except:
        return None
    if not text:
        return None
    entity_data = text['entities'][qid]
    title = ''
    if 'en' in entity_data['labels']:
        title = entity_data['labels']['en']['value']
    types, twitter, political_alignment = get_data_from_statements(entity_data)
    return [title, types, twitter, political_alignment]


def get_meta_data(input):
    """ Get the meta data for each entity associated to a domain in the input file
    :param input: name of the input file
    :return: domains (urls) in the form {<domain>: [qid: <qid>, ref_lang: <language where the reference is used
             (ca or ar)>, en_title: <title in English>, types: [<types as qids>], twitter: {<username>: <number subscribers>},
             political_alignment: [<political alignment as qids>]]}
    """
    domains = {}
    input_data = get_input_file_data(input)
    for url, qid_lists in input_data.items():
        for meta in qid_lists:
            wikidata_result = make_request(meta['qid'])
            if not wikidata_result:
                continue
            title, types, twitter, political_alignment = wikidata_result
            if url not in domains:
                domains[url] = []
            domains[url].append({'qid': meta['qid'], 'ref_lang': meta['language'], 'en_title': title, 'types': types,
                                 'twitter': twitter, 'political_alignment': political_alignment})
            print(url, domains[url])
    return domains


def write_domains(output, domains):
    """ Write domains dict to json file
    :param output: output file to write to (json)
    :param domains: domains dict to write
    """
    json.dump(domains, open(output, 'w'))


def main(input, output):
    domains = get_meta_data(input)
    write_domains(output, domains)


if __name__ == '__main__':
    args = get_args()
    main(args.input, args.output)