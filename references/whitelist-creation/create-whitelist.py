import argparse
import logging
import urllib.request
from urllib.parse import urlparse
import json
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
    try:
        with urllib.request.urlopen(link) as url:
            page_data = json.loads(url.read().decode())
            for ref_sec in page_data['remaining']['sections']:
                if 'isReferenceSection' in ref_sec and ref_sec['isReferenceSection']:
                    reference_sections.append(ref_sec['text'].strip().replace('\n', ''))
    except:
        logging.warning('Link does not work: ' + link)
        return None
    return reference_sections


def get_reference_sections(lang, titles):
    reference_sections = {}
    for title in titles:
        reference_sections[title] = get_reference_section(lang, title)


def get_references(reference_sections):
    reference_data = {}
    for title, reference_section in reference_sections.items():
        reference_data[title] = []
        for page in reference_section:
            soup = BeautifulSoup(page, "html.parser")
            for a in soup.find_all('a', {'rel': 'mw:ExtLink'}):
                reference_data[title].append(a.get('href'))
    return reference_data


def get_counted_domains(references):
    counted_data = {}
    for title, references in references.items():
        for ref in references:
            link = urlparse(ref).netloc.replace('www.', '')
            if link in counted_data:
                counted_data[link] += 1
            else:
                counted_data[link] = 1
    counted_data_sorted = {}
    for k in sorted(counted_data, key=counted_data.get, reverse=True):
        counted_data_sorted[k] = counted_data[k]
    return counted_data_sorted


def write_to_file(output, data):
    with open(output, 'w') as outfile:
        json.dump(data, outfile)


def main(args):
    titles = get_titles(args.input)
    reference_sections = get_reference_sections(args.lang, titles)
    references = get_references(reference_sections)
    domains = get_counted_domains(references)
    write_to_file(domains, args.output)

if __name__ == '__main__':
    args = get_args()
    main(args)