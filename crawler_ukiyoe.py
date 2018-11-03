# import requests
import time
import traceback
import logging
# import collections
import pickle
from urllib.request import Request, urlopen
from utils.headerGen import random_headers
from bs4 import BeautifulSoup as bs

def get_web_page():
    with open('ukiyo-e_rawPage.txt', 'rb') as file:
        page = file.read()
    return page

# def get_paint_url(soup):    
#     paint_rows = soup.find_all('li', attrs={'class':'painting-list-text-row'})
#     paint_urls = [row.a['href'] for row in paint_rows]
#     return paint_urls

def get_pic_url(soup):
    urls = soup.find_all('img', attrs={'class':'ms-zoom-cursor'})
    urls = [url['ng-src'].split('!')[0] for url in urls]
    return urls

def save_pickle(obj, dir):
    with open(dir, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)
    print('Saved as pickle to {}'.format(dir))

if __name__ == '__main__':
    base_url = 'https://www.wikiart.org'

        
    
    page = get_web_page()
    soup = bs(page, 'html.parser')

    urls = get_pic_url(soup)
    url_dict = {'ukiyo-e': urls}
    save_pickle(url_dict, 'ukiyoe_url.pkl')
        
        
