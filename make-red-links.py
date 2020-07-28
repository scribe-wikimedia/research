import argparse

# usage:
# python3 make-red-links.py wikidata-glam/v2-articles.tsv red-link-lists/

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='tsv input file')
    parser.add_argument('outdir', help='output directory')
    args = parser.parse_args()
    return args


def get_labels(input):
    labels = {}
    with open(input) as infile:
        for line in infile:
            if 'http://www.wikidata.org/entity/Q' not in line:
                continue
            lang_code = line.strip().split('\t')[2]
            label = line.strip().split('\t')[1]
            if lang_code not in labels:
                labels[lang_code] = []
            labels[lang_code].append(label)
    return labels


def write_outfile(labels, outdir):
    for lang_code, label_list in labels.items():
        with open(outdir + 'redlinks.' +lang_code + '.wikitext', 'w') as outfile:
            for label in label_list:
                outfile.write('* [[' + label + ']]' + '\n')


def main(input, outdir):
    labels = get_labels(input)
    write_outfile(labels, outdir)


if __name__ == '__main__':
    args = get_args()
    main(args.input, args.outdir)