#!/usr/bin/env python
"""
This is the Flask REST API that processes and outputs the prediction on the URL.
"""
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
# import label_data
from flask import Flask, redirect, url_for, render_template, request,jsonify
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

with tf.device('/cpu:0'):
    model_pre = "./checkpointModel/bestModelCNN"
    model = ConvModel(num_chars, embedding_vector_length, maxlen)
    model.built = True
    model.load_weights(model_pre)

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
def preprocess_url(url, tokenizer):
    url = url.strip()
    sequences = tokenizer.texts_to_sequences([url])
    word_index = tokenizer.word_index
    url_prepped = pad_sequences(sequences, maxlen=maxlen)
    
    return url_prepped

@app.route('/survey', methods=["GET","POST"])
def survey():

    features =  {
        'Chứa địa chỉ IP trong URL' :'Các trang web lừa đảo thường không đăng ký tên miền thay vào đó là sử dụng nguyên IP vì vậy hãy cẩn thận', 
        'Chứa ký tự @ trong URL' : 'Dấu @ có tác dụng bỏ quả tất cả ký tự xuất hiện trước nó (VD: http://totally-legit-site.com@192.168.50.20/account sẽ đưa nạn nhân đến trang 192.168.50.20/account là trang web lửa đảo', 
        'Địa chỉ trang web chứa nhiều path' : 'Tìm kiếm điểm chung của trang web lừa đảo giựa vào số đường dẫn có trong url',
        'Có ký tự // trong tên miền' : 'Ký tự // nằm trong đường dẫn nhằm chuyển hướng người dùng đến trang web lừa đảo', 
        'HTTPS hoặc HTTP trong tên miền' : 'sử dụng https trong domain khiến người dùng nhìn nhầm và chủ quan (VD: http:https://vietcombank.com.vn)', 
        'Sử dụng địa chỉ rút gọn' : 'Sử dụng địa chỉ rút gọn như bit.ly để giấu đi địa chỉ thật sự của trang web lừa đảo', 
        'Có chứa ký tự - trong domain': 'sử dụng ký tự - trong tên miền khiến tên trang web nhìn "có vẻ" không lừa đảo', 
        'Kiểm tra xem DNS có nhận được website không' : 'Kiểm tra xem DNS có trỏ đến được trang web không, nếu không thì trang web đó được đăng ký với dịch vụ không rõ ràng', 
        'Tuổi thọ của tên miền có dưới 6 tháng' : 'Nhưng trang web lừa đảo thường bị báo cáo liên tục đẫn đến việc gỡ xuống và nhưng tên lừa đảo thường không hay bỏ chi phí duy trì server nên tuổi thọ thường rất ngắn', 
        'Tên miền đã hết hạn' : 'Tên miền đã hết hạn đăng ký', 
        'Website có sử dụng Iframe' : 'Sử dụng Iframe chạy chầm trong các trang web để ăn cắp thông tin cá nhân', 
        'Website có sử dụng Mouse_Over' : 'Sử dụng hàm mouse_over trong javscript để khi người dùng đung đưa con chuột qua 1 cái link bất kỳ trang web lừa đảo sẽ tự động bật lên',
        'Website tắt chức năng Right_Click' : 'Trang web vô hiệu hóa chuột phải vì lo sợ ta sẽ nhìn thấy những đoạn mã độc trong trang web', 
        'Sô lần bị forward có quá 2 lần khi vào trang web' : 'Khi vào 1 trang web số lần ta bị tự động forward quá nhiều nhằm qua mặt các công cụ quét',
        'Địa chỉ Website có chứa punny code' : 'Sử dụng punnycode để đánh lừa url (VD: dı sẽ nhìn khá giống với di nhưng punnycode của adıdas.de là trang web lừa đảo với đủ ký tự là http://xn--addas-o4a.de/ nhưng trình duyệt sẽ encode và hiển thị giống như là adidas.de'
    }
    sublist = [list(features.keys())[n:n+3] for n in range(0, len(list(features.keys())), 3)]
    if request.method == "POST" and request.form['url'] != None:
        url = request.form['url']

        if url == '':
            return jsonify({'notvalid' : 'Maybe your input not correct'})

        print(url)

        if(isinstance(url, str)):
            url_prepped = preprocess_url(url, tokenizer)
            prediction = model.predict(url_prepped)
            
            if prediction > 0.5:
                return jsonify({'notsafe' : 'Website Phishing ','score': str(prediction[0][0])})
            else:
                return jsonify({'safe' : 'Website Legitimate','score': str(prediction[0][0]) })


        # return render_template('index.html',data=sublist,features=features)
        
    return render_template('index.html',data=sublist,features=features)

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

@app.route("/predict", methods=["GET","POST"])
def predict():

    # Initialize the dictionary for the response.
    data = {"success": False}

    # Check if POST request.
    if request.method == "GET":
        # Grab and process the incoming json.
        start = time.time()
        incoming = request.get_json()
        url = incoming["url"]

        if url == '':
            return jsonify({'message' : 'Maybe your input not correct'})
            
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

