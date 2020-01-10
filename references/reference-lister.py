import urllib.request
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_pages(lang_code, title):
    reference_sections = []
    link = 'https://' + lang_code + '.wikipedia.org/api/rest_v1/page/mobile-sections/' + title
    try:
        with urllib.request.urlopen(link) as url:
            page_data = json.loads(url.read().decode())
            for ref_sec in page_data['remaining']['sections']:
                if 'isReferenceSection' in ref_sec and ref_sec['isReferenceSection']:
                    reference_sections.append(ref_sec['text'].strip().replace('\n', ''))
    except:
        print('NOOOOOO ----->' + link)
        return None
    return reference_sections

# mw-references
# mw:ExtLink
def get_full_references(lang_code, filepath):
    reference_data = {}
    with open(filepath) as infile:
        next(infile)
        for line in infile:
            #link = line.split('\t')[1].strip()
            link = line.split('\t')[2].strip()
            print(link)
            title = link.replace('https://' + lang_code + '.wikipedia.org/wiki/', '')
            pages = get_pages(lang_code, title)
            if not pages:
                continue
            for page in pages:
                soup = BeautifulSoup(page, "html.parser")
                for a in soup.find_all('a', {'rel': 'mw:ExtLink'}):
                    if link in reference_data:
                        reference_data[link].append(a.get('href'))
                    else:
                        reference_data[link] = [a.get('href')]
    return reference_data

#full_reference_data = get_full_references('ar', '../wikidata-glam/arabic/museum.tsv')
full_reference_data = get_full_references('de', '../wikidata-female-scientists/german/articles.tsv')#

json.dump(full_reference_data, open('female-scientists-de-full-references.json', 'w'))

counted_data = {}
for page, references in full_reference_data.items():
    for ref in references:
        link = urlparse(ref).netloc.replace('www.', '')
        if link in counted_data:
            counted_data[link] += 1
        else:
            counted_data[link] = 1
counted_data_sorted = {}

for k in sorted(counted_data, key=counted_data.get, reverse=True):
    counted_data_sorted[k] = counted_data[k]

print(counted_data_sorted)
json.dump(counted_data_sorted, open('female-scientists-de-references-counted.json', 'w'))



