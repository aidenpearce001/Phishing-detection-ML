from flask import Blueprint, render_template
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import pymongo

#for color 
from matplotlib.colors import Normalize
from matplotlib import colors
import matplotlib.cm as cm


load_dotenv()

MONGODB = os.getenv('MONGODB')

print("MONGO PATH", MONGODB)

client = pymongo.MongoClient(MONGODB)
db = client['chongluadao']

country_mapping = {}  
country2digit = pd.read_csv("country_mapping.csv")
for idx,_country in enumerate(country2digit['Code']):
    country_mapping[_country]= country2digit['Name'][idx]


def hex_color():

    color_list = []

    colors_data = np.random.randn(10, 10)
    cmap = cm.get_cmap('Blues')

    norm = Normalize(vmin=colors_data.min(), vmax=colors_data.max())
    rgba_values = cmap(norm(colors_data))

    for layer1 in rgba_values:
        for layer2 in layer1:
            color_list.append(colors.to_hex([ layer2[0], layer2[1], layer2[2] ]))

    return color_list


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=["GET","POST"])
def main():
    country_data, top_tlds, top_title, importances, url_based, domain_based, content_based, percent_list = \
      [], [], [], [], [], [], [], [],  
    
    contry_pipeline = [
    {
        '$group': {
            '_id': '$country_name', 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }]

    TLDs_pipeline = [
    {
        '$group': {
            '_id': '$TLDs', 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    },{
        '$limit': 10
    }
    ]

    Title_pipeline = [
    {
        '$group': {
            '_id': '$Title', 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    },{
        '$limit': 10
    }
    ]

    total = db['DATA'].count_documents({})
    contry_query = list(db['DATA'].aggregate(contry_pipeline))
    top_country = list(contry_query)
    colors = hex_color()

    print("TOP", top_country)
    top_country = []
    
    if len(top_country) > 0: # If found at least an item
      start = 0
      if top_country[0]['_id'] == None:
          start = 1 
      top_country = top_country[start:start+len(colors)]

      for idx,_data in enumerate(colors):
          try:
              country_dict = {}
              country_dict['id'] = top_country[idx]['_id']
              country_dict['name'] = country_mapping[top_country[idx]['_id']]
              country_dict['value'] = top_country[idx]['count']
              country_dict['fill'] = _data
          except:
              continue

          country_data.append(country_dict)

      top_tlds = list(db['DATA'].aggregate(TLDs_pipeline))
      top_title = list(db['DATA'].aggregate(Title_pipeline))
      importances = list(db["Models"].find({}, {"_id": 0}))

      url_based = ['Speical_Char','URL_Depth','use_http', 'redirection','URL_length','time_get_redirect','Prefix/Suffix','TinyURL','port_in_url','Have_At','http_in_domain','Have_IP','Punny_Code']
      domain_based = ['same_asn','domain_lifespan','domain_timeleft','DNS_Record','trusted_ca']
      content_based = ['iFrame','Web_Forwards','Mouse_Over','Right_Click','fromCharCode','ActiveXObject','escape','eval','atob','unescape']
      percent_list = []

      for _features in (url_based,domain_based,content_based):
          percent = 0
          for i in _features:
              percent += importances[0][i]
          percent_list.append(percent*100)
          
      print(percent*100)
      print(country_data)
      print(top_tlds)
      print(top_title)
    
    if len(percent_list) == 0:
      percent_list = [0,0,0]
    if len(importances) == 0:
      importances = [0]

    return render_template(
      "dashboard.html",
      country_data=country_data,
      top_tlds=top_tlds,
      top_title=top_title,
      importances=importances[0],
      url_based=url_based,
      domain_based=domain_based,
      content_based=content_based,
      percent_list=percent_list
    )

    return render_template("dashboard.html")
      
@dashboard.route('/comparison', methods=["GET","POST"])
def comparison():
    return render_template('dashboard-model.html')
