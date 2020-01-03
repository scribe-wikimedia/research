import pandas as pd
import csv

class fromCSVWriter:

    def get_csv(self, filepath):
        final_data = {}
        data = pd.read_csv(filepath, sep='\t', header=0, encoding='utf-8').to_dict('list')
        for i in xrange(0, len(data['qid'])):
            qid = data['qid'][i].strip().replace('http://www.wikidata.org/entity/', '')
            if not qid in final_data:
                final_data[qid] = []
            tmp = {'name': data['name'][i], 'refurl': data['reference'][i], 'domain': data['type'][i], 'language': data['language'][i], 'summary': data['summary'][i]}
            final_data[qid].append(tmp)
        print(final_data)
        return final_data

    #def prepareSQL(self, data):
