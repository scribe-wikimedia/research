import requests
from bs4 import BeautifulSoup


page = requests.get("https://yallabook.com/guide/show.php?nid=1016&%D9%85%D8%AA%D8%AD%D9%81-%D8%A7%D8%B3%D9%88%D8%A7%D9%86")
#page = requests.get("https://www.bedeutungonline.de/was-bedeutet-deutsche-kartoffel-kartoffeldeutsche/")
#page = requests.get("https://en.wikipedia.org/wiki/Tone_policing")
page = requests.get("https://www.albayan.ae/books/library-visit/2014-11-07-1.2238264")

#print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')


title = soup.find("meta",  property="og:title")
if not title:
    title = soup.title.string
    if not title:
        soup.select('h1')[0]['content']
else:
    title = title['content']

sitename = soup.find("meta", property="og:site_name")

url = soup.find("meta",  property="og:url")
published_time = soup.find("meta",  property="article:published_time")

#print(soup.select('h1'))
#print(soup.title.string)
#print(soup.select('datePublished'))

print(published_time["content"] if published_time else "No published_time")
print(title if title else "No meta title given")
print(sitename["content"] if sitename else "No site name given")
print(url["content"] if url else "No meta url given")