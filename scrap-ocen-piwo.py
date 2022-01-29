#!/usr/bin/env python3

# This is throwaway one-time single-use disposable script to scrap reviews from ocen-piwo.pl. It works though.*
# Sometimes you will need to run it twice to broken issues on first run time.

from bs4 import BeautifulSoup as bs
from threading import Thread
from tqdm import tqdm
import json
import os.path
import pickle
import requests
import requests
from icecream import ic
from tqdm.contrib.concurrent import process_map  # or thread_map
import re
import traceback

if not os.path.exists('ids'): # then recreate file with beer ids
    url = 'https://ocen-piwo.pl/katalog-piw-'

    def fetch_pages(start=0, stop=2080, file_dest='all'):
        beer_ids = []
        for page in tqdm(range(start, stop)):
            page_url = url + str(page * 10)
            # print(page_url)
            req = requests.get(page_url)
            soup = bs(req.text, 'html.parser')
            beers = soup.find_all('a', text='więcej »', href=True)
            page_beer_ids = list(map(lambda tag: tag['href'], beers))
            beer_ids.extend(page_beer_ids)
            if page % 100 == 0:
                with open(file_dest, 'wb') as f:
                    pickle.dump(beer_ids, f)
            with open(file_dest, 'wb') as f:
                pickle.dump(beer_ids, f)

    threads = []

    threads.append(Thread(target=fetch_pages, args=(0, 500, '0-500')))
    threads.append(Thread(target=fetch_pages, args=(500, 1000, '500-1000')))
    threads.append(Thread(target=fetch_pages, args=(1000, 1500, '1000-1500')))
    threads.append(Thread(target=fetch_pages, args=(1500, 2080, '1500-2080')))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    beer_ids = []
    with open('0-500', 'rb') as f:
        beer_ids.extend(pickle.load(f))
    with open('500-1000', 'rb') as f:
        beer_ids.extend(pickle.load(f))
    with open('1000-1500', 'rb') as f:
        beer_ids.extend(pickle.load(f))
    with open('1500-2080', 'rb') as f:
        beer_ids.extend(pickle.load(f))

    with open('0-2800', 'wb') as f:
        pickle.dump(beer_ids, f)

    with open('ids', 'w') as f:
        print(*beer_ids, sep='\n', file=f)

try: # make use of some antipatterns or something if we need to fetch ids from file
    beer_ids
except NameError:
    with open('ids', 'r') as f:
        beer_ids = f.read().splitlines()

num_re = re.compile('[0-9]+')

def parse_comment_div(div):
    # for br in div.find_all("br"):
    #     br.replace_with("\n")
    # ic(div)
    subdivs = div.find_all('div', recursive=False)
    has_rating = len(subdivs) > 1
    # ic(children)
    # ic(subdivs)
    subdivs[0].clear()
    # raise BaseException
    if not has_rating:
        return None
    rating_text = subdivs[1].extract().get_text()
    # ic(children)
    # ic()
    review_text = div.text
    # ic(review_text)
    # ic(rating_text)
    # for div in div.find_all("div"): # i am not sure how to get text that is not in any tag, so ill remove all tags then
    #     div.extract()
    
    return (
        review_text,
        tuple(num_re.findall(rating_text))
    )

SESSID = 'FILL-IN-WITH-COOKIE-FROM-BROWSER'

def collect_beer_reviews(id_idx):
    id = beer_ids[id_idx]
    if os.path.exists(f'./reviews/{id_idx}'): # review already fetched -> do nothing
        return True
    try:
        review_url = f'https://ocen-piwo.pl/{requests.utils.quote(id)}'
        url = 'https://ocen-piwo.pl/script/s1.php?param=zmien_komentarze'
        header = {
            'origin' : 'https://ocen-piwo.pl',
            'referer': review_url,
            'cookie' : f'PHPSESSID={SESSID}',
            'content-type' : 'application/x-www-form-urlencoded'
            }
        review_page = requests.get(review_url).text
        soup = bs(review_page, 'html.parser')
        comment_divs = soup.find_all('div', class_='comment')
        next_page = bool(soup.find('a', text='starsze »', class_='button'))
        limit = 4
        news_id = id.split('-')[-1].lstrip('n')
        # ic(news_id)
        while next_page: # proceed with 'api' for comments on next pages
            data = f'news={news_id}&limit={limit}&page=1'
            table = requests.post(url, headers=header, data=data).text
            # ic(table)
            soup = bs(table, 'html.parser')

            comment_divs.extend(soup.find_all('div', class_='comment'))
            # if comment_divs:
            #     ic(header['referer'])
            #     ic(comment_divs)
            #     ic(comment_divs[0])
            #     ic(comment_divs[0].text)
            #     raise BaseException

            have_next_page = bool(soup.find('a', text='starsze »', class_='button'))
            # ic(have_next_page)
            if not have_next_page:
                break
            # break
            limit += 4
        # ic(comment_divs)
        reviews = list(filter(None, map(parse_comment_div, comment_divs)))
        # if comment_divs:
        #     ic(comment_divs)
        #     raise BaseException
        if reviews:
            with open(f'./reviews/{id_idx}', 'wb') as f:
                pickle.dump(reviews, f)
            # ic(id)
            # ic(reviews)
        return True
    except Exception as e:
        traceback.print_exc()
        return False

# collect_beer_reviews(5429) # just tyskie 0%

# processed_beer_ids = process_map(collect_beer_reviews, [5429], max_workers=2)
processed_beer_ids = process_map(collect_beer_reviews, range(0, 20784), max_workers=50, chunksize=1)

# ic(processed_beer_ids)

with open('./processed_beers', 'wb') as f:
    pickle.dump(processed_beer_ids, f)

reviews_texts = {}

for beer_idx, beer_id in enumerate(beer_ids):
    if os.path.exists(f'./reviews/{beer_idx}'):
        with open(f'./reviews/{beer_idx}', 'rb') as f:
            reviews_texts[beer_id] = pickle.load(f)

if not os.path.exists(f'./ocen-piwo'):
    with open('./ocen-piwo', 'wb') as f:
        pickle.dump(reviews_texts, f)
    with open('./ocen-piwo-utf8.json', 'w') as f:
        json.dump(reviews_texts, f, indent=4, ensure_ascii=False)
