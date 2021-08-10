from flask import Blueprint, request, jsonify, render_template
import time
import os
from model import RandomForest, ConvModel
import re

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


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

features =  {
    'Speical_Char':'Number of Speicial Character in URL like ~,!,@,#,$,%,^,&,*,...',
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



predictor = Blueprint('predictor', __name__)

# Preprocess the url before putting in the predictor
def preprocess_url(url): 
    regex_str = r"(http(s)?:\/\/)(([a-z0-9\-ßàÁâãóôþüúðæåïçèõöÿýòäœêëìíøùîûñé]+\.)+[a-z\-]{2,63})" 
    match = re.search(regex_str, url) 
    if match is not None: 
        s, e = match.span() # Start and end of match 
        return url[s:e] 
    else: 
        return url


@predictor.route('/', methods=["GET","POST"])
def survey():
    sublist = [list(features.keys())[n:n+3] for n in range(0, len(list(features.keys())), 3)]
    if request.method == "POST" and request.form['url'] != None:
        url = request.form['url']

        if url == '':
            return jsonify({'notvalid' : 'Cannot connect to website. Your url might be incorrect, or the website is down'})

        if(isinstance(url, str)):
            url = preprocess_url(url)

            prediction = model.predict(url)
            if(prediction is not None):
                prediction = prediction[0]
            else:
                return jsonify({'notsafe' : 'Cannot connect to website. Your url might be incorrect, or the website is down'})
            
            if prediction > 0.5:
                return jsonify({'notsafe' : 'Website Phishing ','score': str(prediction)})
            else:
                return jsonify({'safe' : 'Website Legitimate','score': str(prediction) })
        # else:
        #     return jsonify({'notsafe' : 'Cannot connect to website. Your url might be incorrect, or the website is down'})
        
    return render_template('index.html',data=sublist,features=features)


@predictor.route("/predict", methods=["POST"])
def predict():

    # Initialize the dictionary for the response.
    data = {"success": False}

    # Grab and process the incoming json.
    start = time.time()
    incoming = request.get_json()
    url = incoming["url"]

    if url == '':
        return jsonify({'message' : 'Cannot connect to website. Your url might be incorrect, or the website is down'})
            
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