#!/usr/bin/env bash

#python3 get-domains.py wikidata-glam/catalan/bing-all-ca-references.json ca-domains-tmp.csv
#python3 get-domains.py wikidata-glam/arabic/bing-all-ar-references.json ar-domains-tmp.csv

cadomains=$(<ca-domains-tmp.csv)
ardomains==$(<ar-domains-tmp.csv)

curl https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.gz | zcat | grep $cadomains > wikidata-ca-entities.txt

curl https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.gz | zcat | grep $ardomains > wikidata-ar-entities.txt

rm ca-domains-tmp.csv
rm ar-domains-tmp.csv


