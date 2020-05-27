import jsonlines
from urllib.parse import urlsplit

def get_base_url(url):
    try:
        netloc = urlsplit(url).netloc
        if netloc.startswith("www."):
            netloc = netloc.replace("www.","")
        return netloc if len(netloc) > 0 else None
    except:
        print("cannot get base url for {}".format(url))
        return None

def count_domains(input):
    with jsonlines.open(input) as infile:
        for obj in infile:
            