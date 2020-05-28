import json
import jsonlines
import argparse
from urllib.parse import urlsplit

# usage:
# python3 calculate-credibility-score.py
#   output-file-name.jsonlines
#   [--bing ../wikidata-glam/arabic/bing-all-ca-references.json or bing-all-ar-references.json]
#   [--wikidata ../wikidata-alignment/wikidata-information.json]
#   [--wikipedia ../wikipedia-references-files/ca.references.aggregated.json or ar.references.aggregated.json]
#   [--wikipedia-domain ../museums-ca-full-references.json or museums-ar-full-references.json]
#   [--enwikipedia-blacklist ../blacklist/Wikipedia-reliable-sources.tsv]
#   [--alexa ]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='jsonlines output file')
    parser.add_argument('--bing', help='Bing results file (json)')
    parser.add_argument('--wikidata', help='Wikidata meta information file (json)')
    parser.add_argument('--wikipedia', help='Wikipedia whitelist over all articles (jsonlines)')
    parser.add_argument('--wikipediadomain', help='Wikipedia whitelist over one domain (json)')
    parser.add_argument('--blacklist', help='Blacklist of domains from English Wikipedia (tsv)')
    parser.add_argument('--alexa', help='Alexa ranking')

    args = parser.parse_args()
    return args


def get_base_url(url):
    """ Given a url, get a base URL
    :param url: URL to shorten
    :return: base URL of the given URL
    """
    try:
        netloc = urlsplit(url).netloc
        if netloc.startswith("www."):
            netloc = netloc.replace("www.","")
        return netloc if len(netloc) > 0 else None
    except:
        print("cannot get base url for {}".format(url))
        return None


def get_bing_domains(bingfile):
    """ Get data from the bing search results
    :param bingfile: json bing search results file
    :return: dict with search results
    """
    return json.load(open(bingfile))


def get_wikidata(wikidatafile):
    """ Get Wikidata meta
    :param wikidatafile: file with the meta data from Wikidata by domain
    :return: dict with wikidata meta data
    """
    wikidata = json.load(open(wikidatafile, 'w'))


def get_wikipedia(wikipediafile):
    """ Get data of how many a url is cited in a wikipedia overall
    :param wikipediafile: aggregated file counted by domain, sorted by base url
    :return: dict with wikipedia reference data
    """
    return json.load(open(wikipediafile))


def get_wikipedia_domains(wikipediadomainfile):
    """ Get data of how often a url is cited in a wikipedia by domain
    :param wikipediadomainfile: aggregated file counted by domain, sorted by base url
    :return: dict with wikipedia domain-specific reference data
    """
    return json.load(open(wikipediadomainfile))


def get_blacklist(blacklistfile):
    """ Get data about which urls are domain on the reliable sources list of English and Arabic Wikipedia
    :param blacklistfile: tsv file containing the table from English and Arabic Wikipedia
    :return: dict in the form {<base url>: [<score>, <language code>]}
    """
    blacklist = {}
    with open(blacklistfile) as infile:
        for line in infile:
            tmp = line.strip().split('\t')
            domain = get_base_url(tmp[1])
            lang_code = tmp[4].lower()
            blacklist[domain] = [tmp[2], lang_code]


def get_score(reference_url, wikidata, wikipedia, wikipediadomain, blacklist):
    """ Check if a given reference domain exists in each scores file and if so, add scores
    :param reference_url: reference url/domain from bing search
    :param wikidata: dict with wikidata meta data
    :param wikipedia: dict with wikipedia usage of a url
    :param wikipediadomain: dict with domain-specific usage of a url
    :param blacklist: blacklist score from Arabic and English Wikipedia
    :return: dict with either the scores or None if no score can be obtained for each metric
    """
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
    if reference_url in blacklist:
        scores['blacklist'] = blacklist[reference_url]
    else:
        scores['blacklist'] = None
    return scores


def get_scores(bing, wikidata, wikipedia, wikipediadomain, blacklist):
    """ Get scores for each of the references in bing search results
    :param bing: bing search results dict
    :param wikidata: dict with wikidata meta data
    :param wikipedia: dict with wikipedia usage of a url
    :param wikipediadomain: dict with domain-specific usage of a url
    :param blacklist: blacklist score from Arabic and English Wikipedia
    :return: domains and all scores
    """
    domains_scores = {}
    for result in bing:
        reference_url = get_base_url(result['url'])
        domains_scores[reference_url] = get_score(reference_url, wikidata, wikipedia, wikipediadomain, blacklist)
        domains_scores[reference_url]['search_result_score'] = result['quality']
    return domains_scores


def write_scores(scores):
    with open('counted-by-domain.tsv') as outfile:
        for domain, score in scores.items():
            outfile.write(domain + '\t' + score)



def main(bingfile, wikidatafile, wikipediafile, wikipediadomainfile, blacklistfile, alexafile, output):
    bing = get_bing_domains(bingfile)
    wikidata = get_wikidata(wikidatafile)
    wikipedia = get_wikipedia(wikipediafile)
    wikipediadomain = get_wikipedia_domains(wikipediadomainfile)
    blacklist = get_blacklist(blacklistfile)

    scores = get_scores(bing, wikidata, wikipedia, wikipediadomain, blacklist)
    write_scores(scores)


if __name__ == '__main__':
    args = get_args()
    main(args.bing, args.wikidata, args.wikipedia,
         args.wikipediadomain, args.blacklist, args.alexa, args.output)
