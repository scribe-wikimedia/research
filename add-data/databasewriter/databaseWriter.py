import pandas as pd
import csv
from databasewriter.webScraper import *
from datetime import date

class fromCSVWriter:

    def get_csv(self, filepath):
        final_data = {}
        data = pd.read_csv(filepath, sep='\t', header=0, encoding='utf-8').to_dict('list')
        for i in range(0, len(data['qid'])):
            qid = data['qid'][i].strip().replace('http://www.wikidata.org/entity/', '')
            if not qid in final_data:
                final_data[qid] = {'references': []}
                final_data[qid]['name'] = data['name'][i]
                final_data[qid]['domain'] = data['type'][i]
            tmp = {'refurl': data['reference'][i], 'language': data['language'][i], 'summary': data['summary'][i]}
            final_data[qid]['references'].append(tmp)
        return final_data

    def get_reference_data(self, data):
        ws = Scraper()
        for qid, data in data.items():
            for i in range(0, len(data['references'])):
                url = data['references'][i]['refurl']
                refdata = ws.run(url)
                data['references'][i].update(refdata)
        print(data)
        return data

    def get_insert_articles(self, data, language_code, articleTag, retrieved_date):
        query = 'INSERT INTO article(name, wd_q_id, lang_code, domain, tag, retrieved_date) VALUES '
        names = ''
        wd_q_ids = ''
        for qid, v in data:



    def run(self, filepath, language_code, articleTag, retrieved_date=date.today()):
        data = self.get_csv(filepath)
        data = self.get_reference_data(data)
        articles_sql = self.get_insert_articles(data, language_code, articleTag, retrieved_date)

