
from cloudevents.sdk.http_events import Event
from flask import Flask, request
import json
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return "Hello World!"


@app.route('/event', methods=['POST'])
def hello():
    # Saving data in event as json object
    headers = dict(request.headers)
    event = Event(headers=headers, data=request.json)
    print(f"Received {event}")
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=3000)
