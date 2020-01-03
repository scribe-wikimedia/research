import pandas as pd
import csv

class fromCSVWriter()

    def get_csv(self, filepath):
        final_data = {}
        data = pd.read_csv(filepath, sep='\t', header=0, encoding='utf-8').to_dict('list')
        for i in xrange(0, len(data['Entity ID'])):
            qid = data['Entity ID'].strip().replace('http://www.wikidata.org/entity/')
            if not qid in final_data:
                final_data['qid'] = {}
                







