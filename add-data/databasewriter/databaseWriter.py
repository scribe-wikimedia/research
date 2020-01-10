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
            tmp = {'refurl': data['reference'][i], 'language': data['language'][i], 'summary': data['summary'][i].replace('"', '\'')}
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
            insert_data = [v['name'], qid, language_code, v['domain'], articleTag, retrieved_date]
            insert_string += query_pre + '(' + (', '.join('"' + item + '"' for item in insert_data)) + ');\n'

        with open(language_code + '-insertArticles.sql', 'w') as outfile:
            print(insert_string)
            outfile.write(insert_string)

    def get_insert_references(self, data, language_code, content_selection_method):
        query_pre = 'INSERT INTO reference(article_id, section_id, publisher_name, publication_title, summary, url, quality, publication_date, retrieved_date, content_selection_method) VALUES '
        insert_string = ''
        for qid, v in data.items():
            for ref in v['references']:
                tmp = ['NULL', ref['publisher_name'], ref['publication_title'], ref['summary'], ref['refurl'], 'NULL', ref['publication_date'], ref['retrieved_date'], content_selection_method]
                insert_data = []
                for k in tmp:
                    if not k:
                        k = 'NULL'
                    insert_data.append(k)
                foreign_key = '(SELECT id FROM article WHERE wd_q_id = "' + qid + '"), '
                insert_string += query_pre + '(' + foreign_key + (', '.join('"' + item.strip() + '"' for item in insert_data)) + ');\n'
        with open(language_code + '-insertReferences.sql', 'w') as outfile:
            print(insert_string)
            outfile.write(insert_string)

    def get_section_templates(self, filepath_sections, domain):
        sections = []
        if domain == 'Museum':
            domain = 'museums'
        with open(filepath_sections + domain.lower() + '-sections.tsv') as infile:
            next(infile)
            for line in infile:
                tmp = line.split('\t')
                sections.append({'order_number': tmp[0], 'quality': tmp[1], 'label': tmp[2]})
        return sections

    def insert_sections(self, filepath_sections, data, language_code, content_selection_method, retrieved_date):
        query_pre = 'INSERT INTO section(article_id, label, order_number, content_selection_method, lang_code, quality, retrieved_date) VALUES '
        insert_string = ''
        for qid, v in data.items():
            domain = v['domain']
            sections = self.get_section_templates(filepath_sections, domain)
            foreign_key = '(SELECT id FROM article WHERE wd_q_id = "' + qid + '"), '
            for sec in sections:
                insert_data = [sec['label'], sec['order_number'], content_selection_method, language_code, sec['quality'], retrieved_date]
                insert_string += query_pre + '(' + foreign_key + (', '.join('"' + item.strip() + '"' for item in insert_data)) + ');\n'
        with open(language_code + '-insertSections.sql', 'w') as outfile:
            print(insert_string)
            outfile.write(insert_string)

    def run(self, filepath_articles, filepath_sections, language_code, articleTag, retrieved_date=date.today()):
        retrieved_date = retrieved_date.strftime('%Y-%m-%d %H:%M:%S')
        data = self.get_csv(filepath_articles)
        data = self.get_reference_data(data)
        self.get_insert_articles(data, language_code, articleTag, retrieved_date)
        self.get_insert_references(data, language_code, articleTag)
        self.insert_sections(filepath_sections, data, language_code, articleTag, retrieved_date)

