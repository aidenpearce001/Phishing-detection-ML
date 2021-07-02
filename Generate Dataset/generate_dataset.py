#!/usr/bin/python3
import pandas as pd
import requests

dataset = set()

def blacklist():
    phishtank = "http://data.phishtank.com/data/online-valid.csv"
    phishtank_res = requests.get('http://data.phishtank.com/data/online-valid.csv', allow_redirects=True)
    open('dataset/phishtank.csv', 'wb').write(phishtank_res.content)
    phistank = pd.read_csv("dataset/phishtank.csv")['url']
    for i in phistank:
        dataset.add( (i,1) )

    git_blacklist = requests.get("https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list")
    file1 = open("dataset/phishing.txt","wb")
    file1.write(git_blacklist.content)
    with open('dataset/phishing.txt', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
    for i in lines[3:]:
        dataset.add( (i,1) )

    phishstat_res = requests.get('https://phishstats.info/phish_score.csv', allow_redirects=True)
    open('dataset/phishstats.txt', 'wb').write(phishstat_res.content)
    with open('dataset/phishstats.txt', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines:
            dataset.add( (i,1) )

def whitelist():
    for i in range(2):
        number = str(i).zfill(2)
        print(f'dataset/majestic_million-0{number}.csv')
        cols = ['GlobalRank', 'TldRank', 'Domain', 'TLD', 'RefSubNets', 'RefIPs',
            'IDN_Domain', 'IDN_TLD', 'PrevGlobalRank', 'PrevTldRank','PrevRefSubNets', 'PrevRefIPs']
        white = pd.read_csv(f'dataset/majestic_million-0{number}.csv',names= cols)["Domain"]
        for i in white:
            dataset.add( ("https://"+i,0) )

cld_dataset = pd.read_csv("dataset/chongluadaov2.csv")
blacklist()
whitelist()

total = lenlist(dataset)
print("TOTAL:",total)
for i in list(dataset):
    new_row = {'url':i[0], 'labels':i[1], 'type':'train'}
    print(new_row)
    cld_dataset.append(new_row, ignore_index=True)

    print(f"{total} row left")
    total -=1
cld_dataset.to_csv("chongluadao_dataset.csv", index = False)
# whitelist = 