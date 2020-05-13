#!/usr/bin/env bash

echo 'get Catalan articles titles'
wget https://dumps.wikimedia.org/cawiki/latest/cawiki-latest-all-titles-in-ns0.gz
gunzip cawiki-latest-all-titles-in-ns0.gz
python3 create-whitelist.py -i cawiki-latest-all-titles-in-ns0 -o ca-references-all.json -l ca

echo 'get Arabic articles titles'
wget https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-all-titles-in-ns0.gz
gunzip arwiki-latest-all-titles-in-ns0.gz
python3 create-whitelist.py -i arwiki-latest-all-titles-in-ns0 -o ar-references-all.json -l ar