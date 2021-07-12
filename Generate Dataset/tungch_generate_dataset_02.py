from queue import Queue
from threading import Thread
import pandas as pd
import requests
import concurrent.futures
import os
from feature_extraction import Extractor
from multiprocessing import Pool
import csv
import time
import gc

THREAD_COUNT = os.cpu_count() * 10
SLEEP_INTERVAL = 5000
SLEEP_INTERVAL_TIME = 5

extractor = Extractor()
feature_names = ['Speical_Char','Have_IP', 'Have_At','URL_length' ,'URL_Depth','redirection', 'time_get_redirect',
                        'port_in_url','use_http', 'http_in_domain','TinyURL', 'Prefix/Suffix', 'DNS_Record','trusted_ca',
                        'domain_lifespan', 'domain_timeleft', 'same_asn','iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards','eval','unescape',
                        'escape', 'ActiveXObject','fromCharCode','atob','Punny_Code', 'country_name']

def blacklist_dataset():
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

def whitelist_dataset():
    dataset = set()
    for i in range(2):
        number = str(i).zfill(2)
        print(f'dataset/majestic_million-0{number}.csv')
        cols = ['GlobalRank', 'TldRank', 'Domain', 'TLD', 'RefSubNets', 'RefIPs',
            'IDN_Domain', 'IDN_TLD', 'PrevGlobalRank', 'PrevTldRank','PrevRefSubNets', 'PrevRefIPs']
        white = pd.read_csv(f'dataset/majestic_million-0{number}.csv',names= cols)["Domain"]
        for i in white:
            dataset.add( ("https://"+i.strip(),0) )
    
    return dataset

def get_dataset():
    dataset = blacklist_dataset() | whitelist_dataset() # Merge blacklist and whitelist
    return dataset

def check_alive(data):
    features = extractor(data[0])
    return data[0], features, data[1]

def writer_handler(writer_q):
    with open("cld.csv", "w") as fout:
        writer = csv.writer(fout, delimiter=",", quotechar='"')
        while True:
            output = writer_q.get()
            if isinstance(output[1], list) and len(output[1]) > 0:
                print("Writting", output)
                writer.writerow(output)

            fout.flush()
            writer_q.task_done()
            gc.collect()


def task_handler(task_q, writer_q):
    while True:
        item = task_q.get()
        writer_q.put(check_alive(item))
        task_q.task_done()
        gc.collect()


def main():
    import time
    
    t0 = time.time()
    dataset = get_dataset()
    sites = [url for url in list(dataset)]

    task_q = Queue(maxsize=THREAD_COUNT)
    writer_q = Queue(maxsize=0)

    for i in range(THREAD_COUNT):
        worker = Thread(target=task_handler, args=(task_q, writer_q))
        worker.setDaemon(True)
        worker.start()

    writer_worker = Thread(target=writer_handler, args=(writer_q,))
    writer_worker.setDaemon(True)
    writer_worker.start()

    for site_idx, site in enumerate(sites):
        task_q.put(site)
        print("=== QUEUE ===")
        print("Task: ", task_q.qsize())
        print("Writer: ", writer_q.qsize())
        print("======")

        if (site_idx + 1) % SLEEP_INTERVAL == 0:
            print(f"Handled {site_idx}/{len(sites)}")
            print(f"Time elapsed: {int(time.time() - t0)}")

            print("Sleeping to cooldown. Please hold")
            time.sleep(SLEEP_INTERVAL_TIME)
            gc.collect()

    task_q.join()
    writer_q.join()

    print(f"Time taken: {int(time.time() - t0)}")

if __name__ == "__main__":
    main()
