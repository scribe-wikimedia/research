#!/usr/bin/env bash

echo 'get Catalan articles titles'
wget https://dumps.wikimedia.org/cawiki/latest/cawiki-latest-all-titles-in-ns0.gz
gunzip cawiki-latest-all-titles-in-ns0.gz

echo 'get Arabic articles titles'
wget https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-all-titles-in-ns0.gz
gunzip arwiki-latest-all-titles-in-ns0.gz