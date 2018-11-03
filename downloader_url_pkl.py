import os
import sys
# import traceback
# import logging
import pickle
import requests
import urllib.request
import random
import time
from utils.headerGen import random_headers


def load_pickle(dir):
    with open(dir, 'rb') as f:
        d = pickle.load(f)
    return d

def download_image(genre, url, filename):
    start_time = time.time()
    try:
        raw = requests.get(url, headers=random_headers())
        time.sleep(0.1)
        with open(filename, 'wb') as image:
            image.write(raw.content)
        print(' Time: {:.2f} secs'.format(time.time()-start_time))
        return False

    except requests.exceptions.RequestException as err:
        print('{} => url: {}'.format(err, url))
        return True

    except Exception as err:
        # Logs the error appropriately.
        # print("\nError url: {} {}".format(genre, url))
        # logging.error(traceback.format_exc())
        print('{} => url: {}'.format(err, url))
        return False

if __name__ == '__main__':

    pkl_names = ['claude-monet_url.pkl', 'ukiyoe_url.pkl', 'vincent-van-gogh_url.pkl']
    root_folders = ['monet', 'ukiyoe', 'vangogh']

    for (pkl_name, root_folder) in zip(pkl_names, root_folders):
        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

        url_dict = load_pickle(pkl_name)    
        Npaints = sum([len(v) for v in url_dict.values()])

        count = 0
        for genre, urls in url_dict.items():
            
            genre_path = os.path.join(root_folder, genre)
            if not os.path.exists(genre_path):
                os.makedirs(genre_path)

            for i, url in enumerate(urls):
                print('{:04d}/{} {} Downloading...'.format(count+1, Npaints, root_folder), end='')
                filename = os.path.join(genre_path, '{:04d}.jpg'.format(i))
                exceptionRaise = download_image(genre, url, filename)
                                
                if exceptionRaise:
                    print("Request Exception Raise. Halt from {} for 20 secs".format(time.strftime("%H:%M:%S", time.localtime())))
                    time.sleep(20)
                elif (count + 1 % 100) == 0: # Sleep a while for every 100 photos
                    print("Sleep for 2 secs.")
                    time.sleep(2)
                count += 1
    print('Finished!')
