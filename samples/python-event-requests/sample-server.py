from flask import Flask, request
app = Flask(__name__)

import json
import io
import requests
import sys
from cloudevents.sdk.Event import Event

@app.route('/', methods=['GET'])
def root():
    return "Hello World!"

@app.route('/event', methods=['POST'])
def hello():
    headers = dict(request.headers)
    print(headers)
    data = request.get_json()
    print(data)
    event = Event(headers=headers, data=data)
    print(event)
    return "Hello World!"

if __name__ == '__main__':
    app.run(port=3000)