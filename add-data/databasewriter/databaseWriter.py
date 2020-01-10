import pandas as pd
import csv
from databasewriter.webScraper import *
from datetime import date
import json

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
        for qid, d in data.items():
            for i in range(0, len(d['references'])):
                url = d['references'][i]['refurl']
                refdata = ws.run(url)
                d['references'][i].update(refdata)
        #json.dump(data, open('reference_data.json', 'w'))
        return data

    def get_insert_articles(self, data, language_code, articleTag, retrieved_date):
        query_pre = 'INSERT INTO article(name, wd_q_id, lang_code, domain, tag, retrieved_date) VALUES '
        insert_string = ''
        for qid, v in data.items():
            insert_data = [v['name'], qid, language_code, v['domain'], articleTag, retrieved_date.strftime('%Y-%m-%d %H:%M:%S')]
            insert_string += query_pre + '(' + (', '.join('"' + item + '"' for item in insert_data)) + ');\n'

        with open('insertArticles.sql', 'w') as outfile:
            print(insert_string)
            outfile.write(insert_string)

    def get_insert_references(self):
        query_pre = 'INSERT INTO article(article_id, section_id, publisher_name, publication_title, summary, url, quality, publication_date, retrieved_date, content_selection_method) VALUES '


    def run(self, filepath, language_code, articleTag, retrieved_date=date.today()):
        data = self.get_csv(filepath)
        data = self.get_reference_data(data)
        articles_sql = self.get_insert_articles(data, language_code, articleTag, retrieved_date)

