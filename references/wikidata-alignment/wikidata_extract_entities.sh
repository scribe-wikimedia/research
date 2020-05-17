#!/usr/bin/env bash

#echo "Download Wikidata dump"
#cd ..
#wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.gz
#cd wikidata-alignment

echo "Extract domains"
python3 get-domains.py ../wikidata-glam/catalan/bing-all-ca-references.json ca-domains-tmp.csv
python3 get-domains.py ../wikidata-glam/arabic/bing-all-ar-references.json ar-domains-tmp.csv

echo "Make one references file"
sort ca-domains-tmp.csv ar-domains-tmp.csv | uniq > ar-ca-domains.csv

#cadomains=$(<ca-domains-tmp.csv)
#ardomains==$(<ar-domains-tmp.csv)

echo "Grep for domains"
zcat ../latest-truthy.nt.gz | grep -f ar-ca-domains.csv > wikidata-ca-entities.txt
