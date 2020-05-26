import gzip

ca_urls = set()
ar_urls = set()

with open('ca-domains-tmp.csv') as infile:
    for line in infile:
        ca_urls.add(line.strip)

with open('ar-domains-tmp.csv') as infile:
    for line in infile:
        ar_urls.add(line.strip())

with open('wikidata-ca-domains.csv', 'w') as caout, open('wikidata-ar-domains.csv', 'w') as arout:
    with gzip.open('../latest-truthy.nt.gz') as infile:
        for line in infile:
            domain = line.strip().split()[2].decode('UTF-8')
            domain = domain.replace('<', '').replace('>', '').replace('http://', '')
            domain = domain.replace('https://', '').replace('www.', '')
            if domain in ca_urls:
                print('ca ' + line.strip().decode('UTF-8'))
                caout.write(line.strip().decode('UTF-8') + '\n')
            if domain in ar_urls:
                print('ar ' + line.strip().decode('UTF-8'))
                arout.write(line.strip().decode('UTF-8') + '\n')

