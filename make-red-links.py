import argparse

# usage:
# python3 make-red-links.py wikidata-glam/arabic/no-arabic-wikipedia-arabic-labels.tsv red-link-lists/arabic-museums.wikitext
# or:
# python3 make-red-links.py wikidata-glam/catalan/no-catalan-article-catalan-labels.tsv red-link-lists/catalan-museums.wikitext

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='tsv input file')
    parser.add_argument('output', help='jsonlines output file')
    args = parser.parse_args()
    return args


def get_labels(input):
    labels = []
    with open(input) as infile:
        for line in infile:
            if 'http://www.wikidata.org/entity/Q' not in line:
                continue
            label = line.strip().split('\t')[1]
            labels.append(label)
    return labels


def write_outfile(labels, output):
    with open(output, 'w') as outfile:
        for label in labels:
            outfile.write('* [[' + label + ']]' + '\n')


def main(input, output):
    labels = get_labels(input)
    write_outfile(labels, output)


if __name__ == '__main__':
    args = get_args()
    main(args.input, args.output)