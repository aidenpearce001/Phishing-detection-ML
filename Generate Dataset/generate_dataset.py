#!/usr/bin/python3
import pandas as pd
import requests

dataset = set()

def blacklist():
    phishtank = "http://data.phishtank.com/data/online-valid.csv"
    phishtank_res = requests.get('http://data.phishtank.com/data/online-valid.csv', allow_redirects=True)
    open('dataset/phishtank.csv', 'wb').write(r.content)
    phistank = pd.read_csv("dataset/phishtank.csv")['url']
    for i in phistank:
        dataset.add( (i,1) )

    git_blacklist = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list"
    open('dataset/phishing.txt', 'wb').write(r.content)
    with open('dataset/phishing.txt', 'r+') as f:
        lines = f.readlines()
    for i in lines[3:]:
        dataset.add( (i,1) )

    phishstat_res = requests.get('https://phishstats.info/phish_score.csv', allow_redirects=True)
    open('dataset/phishstats.csv', 'wb').write(r.content)
    phishstats = pd.read_csv('dataset/phishstats.csv')['URL']
    for i in phishstats:
        dataset.add( (i,1) )

def whitelist():
    for i in range(4):
        number = str(i).zfill(2)
        phishstats = pd.read_csv(f'dataset/majestic_million-0{number}.csv')["Domain"]
        for i in phishstats:
            dataset.add( ("https://"+i,0) )

cld_dataset = pd.read_csv("dataset/chongluadaov2.csv")
blacklist = []
# whitelist = 