from databasewriter.databaseWriter import *

writer = fromCSVWriter()

data = writer.run('../wikidata-glam/catalan/examples-1.tsv', '../wikidata-glam/catalan/','ca', 'example-1')
#print(data)