#!/usr/bin/env python
"""
This is the Flask REST API that processes and outputs the prediction on the URL.
"""
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import label_data
from flask import Flask, redirect, url_for, render_template, request
import json
import pickle
import joblib
import time 
from model import ConvModel
# Initialize our Flask application and the Keras model.
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
num_chars = len(tokenizer.word_index)+1
embedding_vector_length = 128
maxlen = 128
max_words = 20000\

from feature_extraction import *

# classifier = joblib.load('rf_final.pkl')
# ext = Extractor()
with tf.device('/cpu:0'):
    model_pre = "./checkpointModel/bestModelCNN"
    model = ConvModel(num_chars, embedding_vector_length, maxlen)
    model.built = True
    model.load_weights(model_pre)


app = Flask(__name__)

def preprocess_url(url, tokenizer):
    url = url.strip()
    sequences = tokenizer.texts_to_sequences([url])
    word_index = tokenizer.word_index
    url_prepped = pad_sequences(sequences, maxlen=maxlen)
    
    return url_prepped

@app.route('/survey', methods=["GET","POST"])
def survey():

    features =  ['Chứa địa chỉ IP trong URL', 'Chứa ký tự @ trong URL', 'Địa chỉ trang web chứa nhiều path','Có ký tự // trong tên miền', 
    'HTTPS hoặc HTTP trong tên miền', 'Sử dụng địa chỉ rút gọn', 'Có chứa ký tự - trong domain', 'Kiểm tra xem DNS có nhận được website không', 
    'Tuổi thọ của tên miền có dưới 6 tháng', 'Tên miền đã hết hạn', 'Website có sử dụng Iframe', 'Website có sử dụng Mouse_Over','Website tắt chức năng Right_Click', 'Sô lần bị forward có quá 2 lần khi vào trang web','Địa chỉ Website có chứa punny code']
    if request.method == "POST" and request.form['url'] != None:

        data = []
        print(request.form['url'])
        url = request.form['url']
        if(isinstance(url, str)):
            url_prepped = preprocess_url(url, tokenizer)
            prediction = model.predict(url_prepped)
        if prediction > 0.5:
            data.append("phishing")
        else:
            data.append("legit")

        data.append(prediction[0][0])
        print(data)
        return render_template('index.html', data=features, result = data)
    return render_template('index.html',data=features)

@app.route("/predict", methods=["GET"])
def predict():

    # Initialize the dictionary for the response.
    data = {"success": False}

    # Check if POST request.
    if request.method == "GET":
        # Grab and process the incoming json.
        start = time.time()
        incoming = request.get_json()
        url = incoming["url"]
        data["predictions"] = []
        if(isinstance(url, str)):
            url_prepped = preprocess_url(url, tokenizer)
            prediction = model.predict(url_prepped)
            print(prediction)
            end = time.time() - start
            
            if prediction > 0.5:
                result = "URL is probably phishing"
            else:
                result = "URL is probably NOT phishing"
            
        # Check for base URL. Accuracy is not as great.
        
            
        # Processes prediction probability.
            prediction = float(prediction)
            prediction = prediction * 100
            
            r = {"result": result, "phishing percentage": prediction, "url": url}
            data["predictions"].append(r)

            # Show that the request was a success.
            data["success"] = True
            data["time_elapsed"] = end

    # Return the data as a JSON response.
    return jsonify(data)

# Start the server.
if __name__ == "__main__":
    print("Starting the server and loading the model...")
    app.run(host='0.0.0.0', port=45000, debug=True)
    
