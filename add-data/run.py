from databasewriter.databaseWriter import *

writer = fromCSVWriter()

data = writer.run('../wikidata-glam/arabic/examples-1.tsv', 'ar', 'example-1')
#print(data)