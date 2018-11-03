# import requests
import time
import traceback
import logging
import collections
import pickle
from urllib.request import Request, urlopen
from utils.headerGen import random_headers
from bs4 import BeautifulSoup as bs

def get_web_page(url):
    # header = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=random_headers())
    page = urlopen(req)

    return page

def get_paint_url(soup):    
    paint_rows = soup.find_all('li', attrs={'class':'painting-list-text-row'})
    paint_urls = [row.a['href'] for row in paint_rows]
    return paint_urls

def get_paint_genre(soup):
    genre = soup.find('span', attrs={'itemprop':'genre'}).string
    return str(genre)

def get_pic_url(soup):
    url = soup.find('img', attrs={'itemprop':'image'})
    url = url['src'].split('!')[0]
    return url

def save_pickle(obj, dir):
    with open(dir, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)
    print('Saved as pickle to {}'.format(dir))

if __name__ == '__main__':
    base_url = 'https://www.wikiart.org'
    artists = ['claude-monet', 'vincent-van-gogh']

    for artist in artists:
        worklist_url = 'https://www.wikiart.org/en/{}/all-works/text-list'.format(artist)
        
        url_dict = collections.defaultdict(list)
        page = get_web_page(worklist_url)
        soup = bs(page, 'html.parser')
        paint_urls = get_paint_url(soup)
        Npaints = len(paint_urls)
        
        for i, paint_url in enumerate(paint_urls[20:25]):
            print("{:04d}/{} => {} Crawler Urls...".format(i+1, Npaints, artist), end='')
            start_time = time.time()
            try:
                paint_page = get_web_page(base_url + paint_url)
                paint_soup = bs(paint_page, 'html.parser') 
                genre = get_paint_genre(paint_soup)   
                url = get_pic_url(paint_soup)   
                url_dict[genre].append(url)
                print(' Time: {:.2f} secs'.format(time.time()-start_time))

            except Exception as e:
                # Logs the error appropriately.
                print("\nError url: {} {}".format(genre, url))
                logging.error(traceback.format_exc())
        save_pickle(url_dict, '{}_url.pkl'.format(artist))
        
        
