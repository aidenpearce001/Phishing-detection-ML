#!/usr/bin/python3
import pandas as pd
import requests
# import concurrent.futures
import os
from feature_extraction import Extractor
import csv
from queue import Queue

#debug lib
import logging
import gc  
import tracemalloc
import psutil

#some mtfk suggest using this cause simultaneously process several million data, then a queue of workers will take up all the free memory
from bounded_pool_executor import BoundedThreadPoolExecutor

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] %(asctime)s: %(name)s %(message)s)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger("cld")
logger.setLevel(logging.INFO)
ch = logging.FileHandler('logging/logging.log', 'w+')

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

THREAD = os.cpu_count() * 10 

extractor = Extractor()
feature_names = ['url','Speical_Char','Have_IP', 'Have_At','URL_length' ,'URL_Depth','redirection', 'time_get_redirect',
                'port_in_url','use_http', 'http_in_domain','TinyURL', 'Prefix/Suffix', 'DNS_Record','trusted_ca',
                'domain_lifespan', 'domain_timeleft', 'same_asn','iFrame', 'Mouse_Over','Right_Click','eval','unescape',
                'escape', 'ActiveXObject','fromCharCode','atob','Punny_Code',
                'TLDs','Title','country_name','label']

def blacklist():

    dataset = set()

    phishtank = "http://data.phishtank.com/data/online-valid.csv"
    phishtank_res = requests.get('http://data.phishtank.com/data/online-valid.csv', allow_redirects=True)
    open('dataset/phishtank.csv', 'wb').write(phishtank_res.content)
    phistank = pd.read_csv("dataset/phishtank.csv")['url']
    for i in phistank:
        dataset.add( (i.strip(),1) )

    git_blacklist = requests.get("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list")
    file1 = open("dataset/phishing.txt","wb")
    file1.write(git_blacklist.content)
    with open('dataset/phishing.txt', 'r+',encoding='utf-8') as f:
       lines = f.readlines()
    for i in lines[3:]:
       dataset.add( (i.strip(),1) )

    phishstat_res = requests.get('https://phishstats.info/phish_score.csv', allow_redirects=True)
    open('dataset/phishstats.txt', 'wb').write(phishstat_res.content)
    with open('dataset/phishstats.txt', 'r+',encoding='utf-8') as f:
       lines = f.readlines()
       for i in lines[9:]:
           dataset.add( (i.replace('"','').split(',')[2].strip(),1) )

    cld_old = pd.read_csv("dataset/chongluadaov2.csv")
    for i in range(len(cld_old)):
        dataset.add( (cld_old['url'][i], cld_old['labels'][i]) )

    return dataset

def whitelist():

    dataset = set()

    for i in range(2):
        number = str(i).zfill(2)
        cols = ['GlobalRank', 'TldRank', 'Domain', 'TLD', 'RefSubNets', 'RefIPs',
            'IDN_Domain', 'IDN_TLD', 'PrevGlobalRank', 'PrevTldRank','PrevRefSubNets', 'PrevRefIPs']
        white = pd.read_csv(f'dataset/majestic_million-0{number}.csv',names= cols)["Domain"]
        for i in white:
            dataset.add( ("https://"+i.strip(),0) )

    return dataset 

def get_dataset():
    dataset = blacklist() | whitelist() # Merge blacklist and whitelist
    # dataset = blacklist()
    return dataset

def check_alive(data):
    _dict = {}

    features = extractor(data[0])
    if len(features) > 0:
        _dict['url'] = data[0]
        for _idx,_value in enumerate(features):
            _idx +=1
            _dict[feature_names[_idx]] = _value

        _dict['label'] = data[1]

        return _dict

def task_handler(task_q,item):
    # print(f"Number of url has been check : {task_q.qsize()}")
    print("has been check %d: %0.3f MB" %
              (task_q.qsize(), psutil.Process().memory_info().rss / 1e6))
    task_q.put(check_alive(item))
    task_q.task_done()

    gc.collect()


def main():
    import time

    futures = Queue()
    dataset = list(get_dataset())

    print(f"There is total {len(dataset)} urls")
    
    with BoundedThreadPoolExecutor(max_workers=THREAD) as executor: 

        for url in dataset:
            executor.submit(task_handler, futures, url)

    with open('dataset_queue.csv','w+', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer = csv.DictWriter(f, fieldnames = feature_names)
        writer.writeheader()
        while not futures.empty():    
            print(f"Url left writing in files: {futures.qsize()}")    
            try:
                writer.writerow(futures.get())
            except:
                continue

if __name__ == '__main__':
    main()
