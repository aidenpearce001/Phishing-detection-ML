#!/usr/bin/python3
import pandas as pd
import requests
import concurrent.futures

dataset = set()

def blacklist():
    #phishtank = "http://data.phishtank.com/data/online-valid.csv"
    #phishtank_res = requests.get('http://data.phishtank.com/data/online-valid.csv', allow_redirects=True)
    #open('dataset/phishtank.csv', 'wb').write(phishtank_res.content)
    phistank = pd.read_csv("dataset/phishtank.csv")['url']
    for i in phistank:
        dataset.add( (i.strip(),1) )

    #git_blacklist = requests.get("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list")
    #file1 = open("dataset/phishing.txt","wb")
    #file1.write(git_blacklist.content)
    with open('dataset/phishing.txt', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
    for i in lines[3:]:
        dataset.add( (i.strip(),1) )

    #phishstat_res = requests.get('https://phishstats.info/phish_score.csv', allow_redirects=True)
    #open('dataset/phishstats.txt', 'wb').write(phishstat_res.content)
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

#cld_dataset = pd.read_csv("dataset/chongluadaov2.csv")
blacklist()
whitelist()

<<<<<<< HEAD
new_row = {'url':'google.com', 'labels':'1', 'type':'train'}
#cld_dataset = cld_dataset.append(new_row,ignore_index=True)

def append_data(data):
    #global cld_dataset
    cld_dataset = []
    new_row = {'url':data[0], 'labels':data[1], 'type':'train'}
    print(new_row)
    cld_dataset.append(new_row)
    return cld_dataset

def main():
    import time
    data = [url for url in list(dataset)]
    print(len(data))
    cld_dataset = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_proc = {executor.submit(append_data, url): url for url in data}
        for future in concurrent.futures.as_completed(future_proc):
            cld_dataset.extend(future.result())
    assert len(data) == len(cld_dataset), "ngu vl"
    return cld_dataset
if __name__ == '__main__':
    cld_dataset = main()
    print(len(dataset))
    if isinstance(cld_dataset, list):
        cld_dataset = pd.DataFrame(cld_dataset)
=======
def append_data(data):
    global cld_dataset
    
    new_row = new_row = {'url':data[0], 'labels':data[1], 'type':'train'}
    print(new_row)
    cld_dataset = cld_dataset.append(new_row,ignore_index=True)

def main():
    
    data = [url for url in list(dataset)]
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_proc = {executor.submit(append_data, url): url for url in data}
        for future in concurrent.futures.as_completed(future_proc):
            print(future.result())
        
if __name__ == '__main__':
    main()

>>>>>>> 8b9d6b8160d9823f937688157a7f71f51cb3ed55
cld_dataset.to_csv("chongluadao_dataset.csv", index = False)
# whitelist = 
