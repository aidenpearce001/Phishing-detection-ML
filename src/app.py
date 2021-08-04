#!/usr/bin/env python
"""
This is the Flask REST API that processes and outputs the prediction on the URL.
"""
from flask import Flask
from router import dashboard, predictor, feedback
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"


app.register_blueprint(dashboard)
app.register_blueprint(predictor)
app.register_blueprint(feedback)

# Start the server.
if __name__ == "__main__":
    print("Starting the server and loading the model...")
    app.run(host='0.0.0.0', port=4500, debug=True)

