import argparse
import json

# python3 wikidata_information_extractor.py -i wikidata-glam/catalan/bing-all-ca-references.json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='search results file')
    parser.add_argument('output', help='json output file')

    args = parser.parse_args()
    return args


def get_domains(input):
    domains = set()
    reference_data = json.load(open(input))
    for r in reference_data:
        domains.add(r['publisher_name'].replace('http://', '').replace('https://', '').replace('www.', ''))
    return domains


def write_domains(output, domains):
    with open(output, 'w') as outfile:
        for d in domains:
            outfile.write(d + '\n')


def main(input, output):
    domains = get_domains(input)
    write_domains(output, domains)

if __name__ == '__main__':
    args = get_args()
    main(args.input, args.output)