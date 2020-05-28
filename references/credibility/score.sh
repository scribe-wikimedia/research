#!/usr/bin/env bash

echo "Scores for Arabic"

python3 calculate-credibility-score.py outfile.ar.jsonl --bing ../wikidata-glam/arabic/bing-all-ar-references.json --wikidata ../wikidata-alignment/wikidata-information.json --wikipedia ../wikipedia-references-files/ar.references.aggregated.json --wikipediadomain ../museums-ar-full-references.json --blacklist ../blacklist/Wikipedia-reliable-sources.tsv

echo "Scores for Catalan"

python3 calculate-credibility-score.py outfile.ca.jsonl --bing ../wikidata-glam/arabic/bing-all-ca-references.json --wikidata ../wikidata-alignment/wikidata-information.json --wikipedia ../wikipedia-references-files/ca.references.aggregated.json --wikipediadomain ../museums-ca-full-references.json --blacklist ../blacklist/Wikipedia-reliable-sources.tsv