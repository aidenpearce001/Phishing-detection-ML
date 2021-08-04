#!/usr/bin/env python
"""
This is the Flask REST API that processes and outputs the prediction on the URL.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from flask import Flask, redirect, url_for, render_template, request,jsonify
import json
import time 
from model import RandomForest, ConvModel
from dotenv import load_dotenv
import pymongo
import os

#for color 
from matplotlib.colors import Normalize
from matplotlib import colors
import matplotlib.cm as cm

load_dotenv()

MONGODB = os.getenv('MONGODB')

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

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

country_mapping = {}  
country2digit = pd.read_csv("country_mapping.csv")
for idx,_country in enumerate(country2digit['Code']):
    country_mapping[_country]= country2digit['Name'][idx]

# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)
# num_chars = len(tokenizer.word_index)+1
embedding_vector_length = 128
maxlen = 128
max_words = 20000

# model_pre = "./checkpointModel/bestModelCNN"
# model = ConvModel(num_chars, embedding_vector_length, maxlen)
# model.built = True
# model.load_weights(model_pre)

model = RandomForest("model/ckpt/rf_data_balance.pkl")

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
client = pymongo.MongoClient(MONGODB)
db = client['chongluadao']


@app.route('/', methods=["GET","POST"])
def survey():
    features =  {'Speical_Char':'Number of Speicial Character in URL like ~,!,@,#,$,%,^,&,*,...',
        'Have_IP': 'Checks if IP address in URL', 
        'Have_At': 'Checks the presence of @ in URL',
        'URL_length': 'Finding the length of URL and categorizing' ,
        'URL_Depth': 'Gives number of / in URL',
        'redirection' :'Checking for redirection // in the URL', 
        'time_get_redirect':'Number of time get redirect after click URL',
        'port_in_url':'Suspicous port appear in the URL',
        'use_http':'Use HTTP insted of HTTPS', 
        'http_in_domain':'HTTP(S) in the URL (example: https://report?https://reportId=https://QYJT9PC9YPFTDC7JJ&https://reportType=https://question)',
        'TinyURL': 'Checking for Shortening Services in URL', 
        'Prefix/Suffix':'Checking for Prefix or Suffix Separated by (-) in the URL', 
        'DNS_Record': 'Check if the DNS record A point to the right Website',
        'trusted_ca': 'Checking if the Certificate provide by trusted provider like cPanel,Microsoft,Go,DigiCert,...',              
        'domain_lifespan':'Checking if Life span of domain under 6 months', 
        'domain_timeleft':'Checking if time left of domain under 6 months', 
        'same_asn':'Check if others server like Domain, Dns Server,... on the same IP',
        'iFrame':'Check if Iframe Function in Web content', 
        'Mouse_Over':'Check if Mouse_Over Function in Web content',
        'Right_Click':'Check if Right_Click Function in Web content', 
        'Web_Forwards':'Checks the number of forwardings in Web content',
        'eval':'Check if Eval Function in Web content',
        'unescape':'Check if Unescape Function in Web content',
        'escape':'Check if Escape Function in Web content', 
        'ActiveXObject':'Check if ActiveXObject Function in Web content',
        'fromCharCode':'Check if fromCharCode Function in Web content',
        'atob':'Check if atob Function in Web content',
        'Punny_Code':'Check if punny code in URL'
    }
    sublist = [list(features.keys())[n:n+3] for n in range(0, len(list(features.keys())), 3)]
    if request.method == "POST" and request.form['url'] != None:
        url = request.form['url']

        if url == '':
            return jsonify({'notvalid' : 'Maybe your input not correct'})

        if(isinstance(url, str)):

            prediction = model.predict(url)
            if(prediction is not None):
                prediction = prediction[0]
            else:
                return jsonify({'notsafe' : 'Maybe your input not correct'})
            
            if prediction > 0.5:
                return jsonify({'notsafe' : 'Website Phishing ','score': str(prediction)})
            else:
                return jsonify({'safe' : 'Website Legitimate','score': str(prediction) })


        # return render_template('index.html',data=sublist,features=features)
        
    return render_template('index.html',data=sublist,features=features)

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    country_data = []

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
    Importances = list(db["Models"].find({}, {"_id": 0}))

    url_based = ['Speical_Char','URL_Depth','use_http', 'redirection','URL_length','time_get_redirect','Prefix/Suffix','TinyURL','port_in_url','Have_At','http_in_domain','Have_IP','Punny_Code']
    domain_based = ['same_asn','domain_lifespan','domain_timeleft','DNS_Record','trusted_ca']
    content_based = ['iFrame','Web_Forwards','Mouse_Over','Right_Click','fromCharCode','ActiveXObject','escape','eval','atob','unescape']
    percent_list = []

    for _features in (url_based,domain_based,content_based):
        percent = 0
        for i in _features:
            percent += Importances[0][i]
        percent_list.append(percent*100)
        
    print(percent*100)
    print(country_data)
    print(top_tlds)
    print(top_title)

    return render_template('dashboard.html',country_data=country_data,top_tlds=top_tlds,top_title=top_title,Importances=Importances[0],url_based=url_based,domain_based=domain_based,content_based=content_based,percent_list=percent_list)

@app.route('/comparison', methods=["GET","POST"])
def comparison():
    return render_template('dashboard-model.html')
    
@app.route("/feedback", methods=["GET","POST"])
def feedback():
    from datetime import datetime

    today = datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        data = {
            "Date" : today,
            "Title" : request.form['title'],
            "Content" : request.form['content'],
        }

        json_object = json.dumps(data, indent = 4)
  
        with open('feedback/'+str(time.time()) + "_feedback.json", "w") as f:
            f.write(json_object)

        return jsonify(success=True)

@app.route("/predict", methods=["POST"])
def predict():

    # Initialize the dictionary for the response.
    data = {"success": False}

    # Grab and process the incoming json.
    start = time.time()
    incoming = request.get_json()
    url = incoming["url"]

    if url == '':
        return jsonify({'message' : 'Maybe your input not correct'})
            
    data["predictions"] = []
    if(isinstance(url, str)):
        prediction = model.predict(url)[0]
        end = time.time() - start
            
        if prediction > 0.5:
            result = "URL is probably phishing"
        else:
            result = "URL is probably NOT phishing"
        
        # Processes prediction probability.
        prediction = float(prediction)
        prediction = prediction * 100
            
        r = {"result": result, "phishing percentage": prediction, "url": url}
        data["predictions"].append(r)

        # Show that the request was a success.
        data["success"] = True
        data["time_elapsed"] = end
    return jsonify(data)

# Start the server.
if __name__ == "__main__":
    print("Starting the server and loading the model...")
    app.run(host='0.0.0.0', port=4500, debug=True)

