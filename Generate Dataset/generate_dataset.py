#!/usr/bin/python3
import pandas as pd
import requests
import concurrent.futures
import os
from feature_extraction import Extractor
<<<<<<< HEAD
  
Thread = os.cpu_count() * 10
=======
import gc  

THREAD = os.cpu_count() * 10
>>>>>>> c68a557636e9450f6325201df12faaa6a2c6b34e
dataset = set()
alive_dataset = []

extractor = Extractor()
feature_names = ['Speical_Char','Have_IP', 'Have_At','URL_length' ,'URL_Depth','redirection', 'time_get_redirect',
                        'port_in_url','use_http', 'http_in_domain','TinyURL', 'Prefix/Suffix', 'DNS_Record','trusted_ca',
                        'domain_lifespan', 'domain_timeleft', 'same_asn','iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards','eval','unescape',
                        'escape', 'ActiveXObject','fromCharCode','atob','Punny_Code', 'country_name']

def blacklist():
    phishtank = "http://data.phishtank.com/data/online-valid.csv"
    phishtank_res = requests.get('http://data.phishtank.com/data/online-valid.csv', allow_redirects=True)
    open('dataset/phishtank.csv', 'wb').write(phishtank_res.content)
    phistank = pd.read_csv("dataset/phishtank.csv")['url']
    for i in phistank:
        dataset.add( (i.strip(),1) )

    # git_blacklist = requests.get("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list")
    # file1 = open("dataset/phishing.txt","wb")
    #file1.write(git_blacklist.content)
    #with open('dataset/phishing.txt', 'r+',encoding='utf-8') as f:
    #    lines = f.readlines()
    #for i in lines[3:]:
    #    dataset.add( (i.strip(),1) )

    # phishstat_res = requests.get('https://phishstats.info/phish_score.csv', allow_redirects=True)
    # open('dataset/phishstats.txt', 'wb').write(phishstat_res.content)
    #with open('dataset/phishstats.txt', 'r+',encoding='utf-8') as f:
    #    lines = f.readlines()
    #    for i in lines[9:]:
    #        dataset.add( (i.replace('"','').split(',')[2].strip(),1) )

    cld_old = pd.read_csv("dataset/chongluadaov2.csv")
    for i in range(len(cld_old)):
        dataset.add( (cld_old['url'][i], cld_old['labels'][i]) )

def whitelist():
    for i in range(2):
        number = str(i).zfill(2)
        print(f'dataset/majestic_million-0{number}.csv')
        cols = ['GlobalRank', 'TldRank', 'Domain', 'TLD', 'RefSubNets', 'RefIPs',
            'IDN_Domain', 'IDN_TLD', 'PrevGlobalRank', 'PrevTldRank','PrevRefSubNets', 'PrevRefIPs']
        white = pd.read_csv(f'dataset/majestic_million-0{number}.csv',names= cols)["Domain"]
        for i in white:
            dataset.add( ("https://"+i.strip(),0) )

blacklist()
whitelist()

def check_alive(data):
<<<<<<< HEAD
    code = requests.get(data[0], timeout=5)
    features = extractor(data[0])
    print(features)
    if len(features) > 0 and code.status_code not in range(400,600):
        alive_dataset.append(( data[0],features, data[1]  ))

#output = pd.DataFrame()
=======
    try:
        code = requests.get(data[0], timeout=5)
        features = extractor(data[0])
        gc.collect()
        if len(features) > 0 and code.status_code not in range(400,600):
            alive_dataset.append(( data[0],features, data[1]  ))
            
            # return data[0],features,data[1]
        else:
            return None
    except:
        gc.collect()
        return None

# output = pd.DataFrame()
>>>>>>> c68a557636e9450f6325201df12faaa6a2c6b34e
def append_data(data):
    cld_dataset = []
      
    new_row = {}

    for index,value in enumerate(data[1]):
        new_row[feature_names[index]] = value

    new_row['labels'] = data[2]
    # new_row = {'url':data[0], 'labels':data[1], 'type':'train'}
    print(new_row)

    cld_dataset.append(new_row)
    #output = output.append(new_row, ignore_index=True)
    #output.to_csv("chongluadao_dataset_process.csv", index = False)

    return cld_dataset

def main():
    import time

    sites = [url for url in list(dataset)]
<<<<<<< HEAD
    with concurrent.futures.ThreadPoolExecutor(max_workers=Thread) as executor:
        executor.map(check_alive, sites)

    print("DONE")
    time.sleep(10)
    print(f"total {len(alive_dataset)}")
=======
   
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD) as executor:
        executor.map(check_alive, sites)

    total =len(alive_dataset)
>>>>>>> c68a557636e9450f6325201df12faaa6a2c6b34e
    data = [url for url in alive_dataset]
    cld_dataset = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
        future_proc = {executor.submit(append_data, url): url for url in data}
        for future in concurrent.futures.as_completed(future_proc):
            cld_dataset.extend(future.result())
    return cld_dataset
    
if __name__ == '__main__':
    cld_dataset = main()
    print(len(dataset))
    if isinstance(cld_dataset, list):
        big_data = pd.DataFrame(cld_dataset)
    big_data.to_csv("chongluadao_dataset.csv", index = False)
