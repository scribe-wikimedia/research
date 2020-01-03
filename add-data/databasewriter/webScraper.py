import requests
from bs4 import BeautifulSoup
from datetime import date

class Scraper():

    def get_title(self, soup):
        title = soup.find("meta", property="og:title")
        if not title:
            title = soup.title.string
            if not title:
                soup.select('h1')[0]['content']
        else:
            title = title['content']
        return title

    def scrape_website(self, url):
        print(url)
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            title = self.get_title(soup)
            sitename = soup.find("meta", property="og:site_name")
            if sitename:
                sitename = sitename['content']
            published_time = soup.find("meta", property="article:published_time")
            if published_time:
                published_time = published_time['content']
            return {'publisher_name': sitename, 'publication_title': title, 'publication_date': published_time, 'retrieved_date': date.today()}
        else:
            return {'publisher_name': None, 'publication_title': None, 'publication_date': None, 'retrieved_date': date.today()}



    def run(self, url):
        return self.scrape_website(url)