#!/usr/bin/python3
import pandas as pd
import requests
import concurrent.futures
import os
from feature_extraction import Extractor
import csv
from queue import Queue

#debug lib
import logging
import gc  
import tracemalloc
import functools

#some mtfk suggest using this cause simultaneously process several million data, then a queue of workers will take up all the free memory
from bounded_pool_executor import BoundedThreadPoolExecutor

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] %(asctime)s:d %(name)s %(message)s)"

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
ch = logging.FileHandler('logging/memory_leak_trace.log', 'w+')

ch.setFormatter(CustomFormatter())
# logger.FileHandler('logging/memory_leak_trace.log', 'w+')
logger.addHandler(ch)
# handler = colorlog.StreamHandler()
# handler.setFormatter(colorlog.ColoredFormatter(
# 	'[%(log_color)s%(levelname)s]:%(name)s:%(message)s'))
# logging.basicConfig(filename='logging/memory_leak_trace.log',
#                             filemode='a',
#                             format='[%(log_color)%s(levelname)s] %(asctime)s,d %(name)s %(log_color)s%(message)s',
#                             datefmt='%H:%M:%S',
#                             level=logging.INFO)

THREAD = os.cpu_count() * 10 

extractor = Extractor()
feature_names = ['url','Speical_Char','Have_IP', 'Have_At','URL_length' ,'URL_Depth','redirection', 'time_get_redirect',
                'port_in_url','use_http', 'http_in_domain','TinyURL', 'Prefix/Suffix', 'DNS_Record','trusted_ca',
                'domain_lifespan', 'domain_timeleft', 'same_asn','iFrame', 'Mouse_Over','Right_Click','eval','unescape',
                'escape', 'ActiveXObject','fromCharCode','atob','Punny_Code',
                'TLDs','country_name','label']

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
    # dataset = blacklist() | whitelist() # Merge blacklist and whitelist
    dataset = blacklist()
    return dataset

def check_alive(data):
    _dict = {}

    features = extractor(data[0])
    if len(features) > 0:
        _dict['url'] = data[0]
        for _idx,_value in enumerate(features):
            _idx +=1
            _dict[feature_names[_idx]] = _value
        # _data = data[0]+','+','.join(str(v) for v in features)+ ',' +str(data[1])

        _dict['label'] = data[1]
        # print("Iteration %d: %0.3f MB" %
        #       (i, psutil.Process().memory_info().rss / 1e6))
        dc = _dict.copy()
        _dict.clear()

        # print(futures.qsize())
        return dc

def get_queue(queue):
    item = queue.get()
    self.__log.info(str(item))
    return True

def main():
    import time

    dataset = list(get_dataset())[:30]
    _size = 10000
    for idx,sub_list in enumerate([dataset[i:i + _size] for i in range(0, len(dataset), _size)]):

        # alive_dataset = []
        # futures = []
        futures = Queue()
        
        # csv_name = 'dataset_'+str(idx) + '.csv'
        # with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD) as executor:
        #     # executor.map(check_alive, sub_list)
        #     for url in sub_list:
        #         # futures.append(executor.submit(check_alive, url))
        #         futures.put(worker.submit(check_alive, url))

        #     # tracemalloc.start()  # save upto 5 stack frames
        #     # first_log = tracemalloc.take_snapshot()

        #     with open(csv_name, 'w+',encoding='utf-8') as f:
        #         writer = csv.writer(f)
        #         writer = csv.DictWriter(f, fieldnames = feature_names)
        #         writer.writeheader()
                
        #         while not futures.empty():
        #             print(f"{futures.qsize()} left")
        #             item = futures.get().result()
        #             if item != None:
        #                 writer.writerow(item)

                # for future in concurrent.futures.as_completed(futures):

                #     print(f"{total} left")
                #     if future.result() != None:
                #         writer.writerow(future.result())
                #         second_log = tracemalloc.take_snapshot()
                #         stats = second_log.compare_to(first_log, 'lineno')
                #         for stat in stats[:10]:
                #             logger.info(stat)

        tracemalloc.start() 
        first_log = tracemalloc.take_snapshot()
        with BoundedThreadPoolExecutor(max_workers=THREAD) as executor:

            _futures = []

            for url in sub_list:
                _futures.append(executor.submit(check_alive, url))

            csv_name = 'dataset_'+str(idx) + '.csv'

            for future in concurrent.futures.as_completed(_futures):
                futures.put(future.result())
                _futures.clear()

            with open(csv_name,'w', newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer = csv.DictWriter(f, fieldnames = feature_names)
                writer.writeheader()
                
                while not futures.empty():
                    print(f"{futures.qsize()} left")
                    
                    try:
                        writer.writerow(futures.get())
                        econd_log = tracemalloc.take_snapshot()
                        stats = second_log.compare_to(first_log, 'lineno')
                        for stat in stats[:10]:
                            logger.info(stat)
                    except:
                        continue

                    # item = futures.get()
                    # if item != None:
                    #     writer.writerow(item)

                    # second_log = tracemalloc.take_snapshot()
                    # stats = second_log.compare_to(first_log, 'lineno')
                    # for stat in stats[:10]:
                    #     logger.info(stat)

            # _futures.clear()
            gc.collect()
            # gc.collect()
            # wrappers = [a for a in gc.get_objects() if isinstance(a, functools._lru_cache_wrapper)]

            # for wrapper in wrappers:
            #     wrapper.cache_clear()
            # time.sleep(3)
                
                    # print(future.result())
        # print(alive_dataset)
        # total = len(alive_dataset)
        # csv_name = 'dataset_'+str(idx) + '.csv'
        # with open(csv_name, 'a') as f:
        #     for _data in alive_dataset:
        #         print(f"{total} left")

        #         writer = csv.writer(f)
        #         writer.writerow(feature_names)
        #         writer.writerow(_data)

        #         total -=1

        # time.sleep(3)
        # gc.collect()
        

    # total =len(alive_dataset)
    # data = [url for url in alive_dataset]
    # cld_dataset = []
    # with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
    #     future_proc = {executor.submit(append_data, url): url for url in data}
    #     for future in concurrent.futures.as_completed(future_proc):
    #         cld_dataset.extend(future.result())
    # return cld_dataset
    
if __name__ == '__main__':
    main()
    # cld_dataset = main()
    # print(len(dataset))
    # if isinstance(cld_dataset, list):
        # big_data = pd.DataFrame(cld_dataset)
    # big_data.to_csv("chongluadao_dataset.csv", index = False)
