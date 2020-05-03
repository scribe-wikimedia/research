import argparse
import logging
import urllib.request
from urllib.parse import urlparse
import json
import jsonlines
from bs4 import BeautifulSoup
# python3 create-whitelist.py -i cawiki-latest-all-titles-in-ns0 -o ca-references-all.json -l ca

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True,
                help='search results file')
    parser.add_argument('--output', '-o', required=True,
                help='json output file')
    parser.add_argument('--lang', '-l', required=True,
                help='language of the Wikipedia, e.g. ca or ar')

    args = parser.parse_args()
    return args


def get_titles(input):
    titles = []
    with open(input) as infile:
        for line in infile:
            titles.append(line.strip())
    return titles


def get_reference_section(lang, title):
    reference_sections = []
    link = 'https://' + lang + '.wikipedia.org/api/rest_v1/page/mobile-sections/' + title
    page_data = None
    try:
        with urllib.request.urlopen(link) as url:
            page_data = json.loads(url.read().decode())
    except:
        logging.warning('Link does not work: ' + link)
        return None
    for ref_sec in page_data['remaining']['sections']:
        if 'isReferenceSection' in ref_sec and ref_sec['isReferenceSection']:
            reference_sections.append(ref_sec['text'].strip().replace('\n', ''))
    if not reference_sections:
        logging.warning('No references for this link: ' + link)
    return reference_sections


def get_references(reference_section):
    reference_data = []
    for page in reference_section:
        soup = BeautifulSoup(page, "html.parser")
        for a in soup.find_all('a', {'rel': 'mw:ExtLink'}):
            reference_data.append(a.get('href'))
    return reference_data


def get_counted_domains(references, counted_data, final=False):
    counted_data_sorted = {}
    if final:
        for k in sorted(counted_data, key=counted_data.get, reverse=True):
            counted_data_sorted[k] = counted_data[k]
        return counted_data_sorted

    for ref in references:
        link = urlparse(ref).netloc.replace('www.', '')
        if link in counted_data:
            counted_data[link] += 1
        else:
            counted_data[link] = 1
    return counted_data


def write_to_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def write_to_file_tmp(filename, data):
    if not data:
        return
    with jsonlines.open(filename, mode='a') as writer:
        writer.write(data)


def get_title_data(lang, title):
    reference_section = get_reference_section(lang, title)
    if not reference_section:
        return None
    reference = get_references(reference_section)
    write_to_file_tmp(lang + '-all-references.jsonl', {title: reference})
    return reference


def iterate_over_titles(input, output, lang):
    references = {}
    counted_domains = {}
    with open(input) as infile:
        for line in infile:
            title = line.strip()
            reference = get_title_data(lang, title)
            if not reference:
                continue
            references[title] = reference
            counted_domains = get_counted_domains(reference, counted_domains)
    counted_domains = get_counted_domains(None, counted_domains, final=True)
    write_to_file(output, counted_domains)


def main(args):
    iterate_over_titles(args.input, args.output, args.lang)

if __name__ == '__main__':
    args = get_args()
    main(args)
