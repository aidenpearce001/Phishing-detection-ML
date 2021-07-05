#!/usr/bin/python3
import pandas as pd
import requests
import concurrent.futures
import os
  
Thread = os.cpu_count() * 10
dataset = set()

def blacklist():
    # phishtank = "http://data.phishtank.com/data/online-valid.csv"
    # phishtank_res = requests.get('http://data.phishtank.com/data/online-valid.csv', allow_redirects=True)
    # open('dataset/phishtank.csv', 'wb').write(phishtank_res.content)
    phistank = pd.read_csv("dataset/phishtank.csv")['url']
    for i in phistank:
        dataset.add( (i.strip(),1) )

    # git_blacklist = requests.get("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list")
    # file1 = open("dataset/phishing.txt","wb")
    # file1.write(git_blacklist.content)
    with open('dataset/phishing.txt', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
    for i in lines[3:]:
        dataset.add( (i.strip(),1) )

    # phishstat_res = requests.get('https://phishstats.info/phish_score.csv', allow_redirects=True)
    # open('dataset/phishstats.txt', 'wb').write(phishstat_res.content)
    with open('dataset/phishstats.txt', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines[9:]:
            dataset.add( (i.replace('"','').split(',')[2].strip(),1) )

def whitelist():
    for i in range(2):
        number = str(i).zfill(2)
        print(f'dataset/majestic_million-0{number}.csv')
        cols = ['GlobalRank', 'TldRank', 'Domain', 'TLD', 'RefSubNets', 'RefIPs',
            'IDN_Domain', 'IDN_TLD', 'PrevGlobalRank', 'PrevTldRank','PrevRefSubNets', 'PrevRefIPs']
        white = pd.read_csv(f'dataset/majestic_million-0{number}.csv',names= cols)["Domain"]
        for i in white:
            dataset.add( ("https://"+i.strip(),0) )

origin_dataset = pd.read_csv("dataset/chongluadaov2.csv")
blacklist()
whitelist()

alive_dataset = []

def check_alive(data):
    try:
        code = requests.get(data[0], timeout=5)
        if code.status_code == 200:
            alive_dataset.append(data)
        else:
            alive_dataset.append(data)
    except:
        pass
    
    print(f"{data[0]} Alive")

def append_data(data):
    cld_dataset = []
      
    new_row = {'url':data[0], 'labels':data[1], 'type':'train'}
    print(new_row)

    cld_dataset.append(new_row)
    return cld_dataset

def main():
    import time

    sites = [url for url in list(dataset)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=Thread) as executor:
        executor.map(check_alive, sites)

    data = [url for url in alive_dataset]
    cld_dataset = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_proc = {executor.submit(append_data, url): url for url in data}
        for future in concurrent.futures.as_completed(future_proc):
            print(future.result())
            cld_dataset.extend(future.result())
    return cld_dataset
if __name__ == '__main__':
    cld_dataset = main()
    print(len(dataset))
    if isinstance(cld_dataset, list):
        cld_dataset = pd.DataFrame(cld_dataset)
        big_data = cld_dataset.append(origin_dataset, ignore_index=True)
        big_data.to_csv("chongluadao_dataset.csv", index = False)
# append_data( ("https://google.com","1"))
big_data.to_csv("chongluadao_dataset.csv", index = False)
