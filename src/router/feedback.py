from flask import Blueprint, request, jsonify
import json
import time




feedback = Blueprint('feedback', __name__)

@feedback.route("/feedback", methods=["GET","POST"])
def main():
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