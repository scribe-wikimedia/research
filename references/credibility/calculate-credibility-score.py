import json
import jsonlines
import argparse
from urllib.parse import urlsplit

# usage:
# python3 calculate-credibility-score.py
#   [--bing ../wikidata-glam/arabic/bing-all-ca-references.json or bing-all-ar-references.json]
#   [--wikidata ../wikidata-alignment/wikidata-information.json]
#   [--wikipedia ../wikipedia-references-files/ca.references.aggregated.json or ar.references.aggregated.json]
#   [--wikipedia-domain ../museums-ca-full-references.json or museums-ar-full-references.json]
#   [--enwikipedia-blacklist ../blacklist/Wikipedia-reliable-sources.tsv]
#   [--alexa ]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='json output file')
    parser.add_argument('--bing', metavar='bingfile', help='Bing results file (json)')
    parser.add_argument('--wikidata', metavar='wikidatafile', help='Wikidata meta information file (json)')
    parser.add_argument('--wikipedia', metavar='wikipediafile', help='Wikipedia whitelist over all articles (jsonlines)')
    parser.add_argument('--wikipedia-domain', metavar='wikipediadomainfile', help='Wikipedia whitelist over one domain (json)')
    parser.add_argument('--enwikipedia-blacklist', metavar='enblacklistfile', help='Blacklist of domains from English Wikipedia (tsv)')
    parser.add_argument('--alexa', metavar='alexa', help='Alexa ranking')

    args = parser.parse_args()
    return args


def get_base_url(url):
    try:
        netloc = urlsplit(url).netloc
        if netloc.startswith("www."):
            netloc = netloc.replace("www.","")
        return netloc if len(netloc) > 0 else None
    except:
        print("cannot get base url for {}".format(url))
        return None


def get_bing_domains(bingfile):
    return json.load(open(bingfile))


def get_wikidata(wikidatafile):
    wikidata = {}
    with jsonlines.open(wikidatafile) as infile:
        for obj in infile:
            for k, v in obj.items():
                wikidata[k] = v
    return wikidata


def get_wikipedia(wikipediafile):
    return json.load(open(wikipediafile))


def get_wikipedia_domains(wikipediadomainfile):
    return json.load(open(wikipediadomainfile))


def get_enblacklist(enblacklistfile):
    enblacklist = {}
    with open(enblacklistfile) as infile:
        for line in infile:
            tmp = line.strip().split('\t')
            enblacklist[tmp[1]] = tmp[2]


def get_score(reference_url, wikidata, wikipedia, wikipediadomain, enblacklist):
    scores = {}
    if reference_url in wikidata:
        scores['wikidata'] = wikidata[reference_url]
    else:
        scores['wikipedia'] = None
    if reference_url in wikipedia:
        scores['wikipedia'] = wikipedia[reference_url]
    else:
        scores['wikipedia'] = None
    if reference_url in wikipediadomain:
        scores['wikipediadomain'] = wikipediadomain[reference_url]
    else:
        scores['wikipediadomain'] = None
    if reference_url in enblacklist:
        scores['enblacklist'] = enblacklist[reference_url]
    else:
        scores['enblacklist'] = None
    return scores


def get_scores(bing, wikidata, wikipedia, wikipediadomain, enblacklist):
    domains_scores = {}
    for result in bing:
        reference_url = get_base_url(result['url'])
        domains_scores[reference_url] = get_score(reference_url, wikidata, wikipedia, wikipediadomain, enblacklist)
    return domains_scores


def write_scores(scores):
    with open('counted-by-domain.tsv') as outfile:
        for domain, score in scores.items():
            outfile.write(domain + '\t' + score)



def main(bingfile, wikidatafile, wikipediafile, wikipediadomainfile, enblacklistfile, alexafile, output):
    bing = get_bing_domains(bingfile)
    wikidata = get_wikidata(wikidatafile)
    wikipedia = get_wikipedia(wikipediafile)
    wikipediadomain = get_wikipedia_domains(wikipediadomainfile)
    enblacklist = get_enblacklist(enblacklistfile)

    scores = get_scores(bing, wikidata, wikipedia, wikipediadomain, enblacklist)
    write_scores(scores)


if __name__ == '__main__':
    args = get_args()
    main(args.bingfile, args.wikidatafile, args.wikipediafile,
         args.wikipediadomainfile, args.enblacklistfile, args.alexafile, args.output)
