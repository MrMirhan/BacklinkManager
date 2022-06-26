import time
from typing import final
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib, re, random, requests, sys
from datetime import datetime
import lxml
from serpapi import GoogleSearch

serpkey = "5bc5c4047d52b709733adf6a35b9d1d84c928e86bd7e9c4799444fa388b6bd7b"

query = 'how can i'
owned_domain = 'reddit.com'

exclude_urls = ['wikipedia',
                'youtube', 'facebook', 'instagram', 'pinterest', 'ebay',
                'tripadvisor', 'reddit', 'twitter', 'flickr', 'amazon', 'etsy',
                'dailymotion', 'linkedin', 'google', 'aliexpress', 'quora', owned_domain]

query += " allinurl: " + owned_domain + ' '

for exclude in exclude_urls:
    query = query + " -inurl:" + exclude

query = urllib.parse.quote_plus(query)

number_result = 2000

ua = requests.get("https://fake-useragent.herokuapp.com/browsers/0.1.11").json()['browsers']['chrome']
google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result) + '&gbv=1&sei=YwHNVpHLOYiWmQHk3K24Cw'
print("Query:", google_url)
response = requests.get(google_url, headers = {"User-Agent": random.choice(ua)})
soup = BeautifulSoup(response.content, "html5lib")
result_div = soup.find_all('div', attrs={'class': 'egMi0 kCrYT'})

if len(result_div) == 0:
    print('Nothing found..')
    exit()

page = 1
while True:
    souplx = BeautifulSoup(response.text, "lxml")
    next_page = souplx.select_one("a#pnnext")
    print(next_page)
    next_page = souplx.select("a#pnnext")
    print(next_page)
    next_page = souplx.find('a', attrs={'id': 'pnnext'})
    print(next_page)
    if next_page is not None:
        print(f"Parsing page:", page, "\r", end='')
        response = requests.get("https://google.com"+next_page['href'])
        soup = BeautifulSoup(response.content, "html5lib")
        result_div += soup.find_all('div', attrs={'class': 'egMi0 kCrYT'})
        page +=1
    else:
        break

links = []
titles = []
descriptions = []
for r in result_div:
    try:
        link = r.find('a', href = True)
        title = r.find('h3', attrs={'class': 'zBAuLc l97dzf'}).get_text()
        
        if link != '' and title != '':
            links.append(link['href'])
    except:
        print('error on splittiong')
        continue

print(f'Founded Links: {len(links)}')

to_remove = []
clean_links = []
for i, l in enumerate(links):
    clean = re.search('\/url\?q\=(.*)\&sa',l)
    if clean is None:
        to_remove.append(i)
        continue
    clean_links.append(clean.group(1))

print(f'Clean Links: {len(clean_links)}')

backlinks = []
error_manual = []

x=0

def print_stats():
    print('({}/{}) [F: {} | E: {}] Searching backlinks.. [{}%]'.format(x, len(clean_links), len(backlinks), len(error_manual), round(x/len(clean_links)*100, 2)), end='\r', flush=True)

for url in clean_links:
    print_stats()
    try:
        if len([url for h in [a['href'] for a in BeautifulSoup(requests.get(url, timeout=4, allow_redirects=False).content, 'html5lib').find_all('a',  href = True)] if owned_domain in h]) > 0 and url not in backlinks: backlinks.append(url)
    except:
        error_manual.append(url)
    finally:
        x+=1

time.sleep(1.5)

if len(backlinks) > 0:
    backlinkFile = open(f'./list/{round(datetime.now().timestamp())}.txt', 'w', newline='')
    for url in tqdm(backlinks, ncols=100):
        backlinkFile.write(url+'\n')
    backlinkFile.close()

print(f'URL has {len(backlinks)} backlinks..')