#!/usr/bin/python3
import pandas as pd
import requests
import concurrent.futures
import os
from feature_extraction import Extractor
from multiprocessing import Pool
import csv
import time

THREAD_COUNT = os.cpu_count() * 10
extractor = Extractor()
feature_names = ['Speical_Char','Have_IP', 'Have_At','URL_length' ,'URL_Depth','redirection', 'time_get_redirect',
                        'port_in_url','use_http', 'http_in_domain','TinyURL', 'Prefix/Suffix', 'DNS_Record','trusted_ca',
                        'domain_lifespan', 'domain_timeleft', 'same_asn','iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards','eval','unescape',
                        'escape', 'ActiveXObject','fromCharCode','atob','Punny_Code', 'country_name']

def blacklist_dataset():
    dataset = set()
    with open('dataset/phishing.txt', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
    for i in lines[3:]:
        dataset.add( (i.strip(),1) )
    
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

def main():
    import time

    dataset = get_dataset()
    sites = [url for url in list(dataset)]

    with Pool(THREAD_COUNT) as p:
        with open("cld.csv", "w") as fout:
            writer = csv.writer(fout, delimiter=",", quotechar='"')
            t0 = time.time()
            for idx in range(0, len(sites), THREAD_COUNT):
                batch_sites = sites[idx:idx+THREAD_COUNT]
                batch_outputs = p.map(check_alive, batch_sites)
                print("output", batch_outputs)
                for output in batch_outputs:
                    if isinstance(output[1], list) and len(output[1]) > 0:
                        writer.writerow(output)
                    else:
                        print(f"Discarding output of {output[0]}")
                        print(output)

                fout.flush()   

                time_elapsed = time.time() - t0
                print(f"=== {idx}/{len(sites)}. Time elapsed (s): {int(time_elapsed)} / {int(time_elapsed/(idx+1)*len(sites))}") 

if __name__ == "__main__":
    main()
