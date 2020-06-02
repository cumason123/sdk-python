
from cloudevents.sdk.events import Event
from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return "Hello World!"


@app.route('/event', methods=['POST'])
def hello():
    # Saving data in event as json object
    data = request.json
    headers = dict(request.headers)
    event = Event(headers=headers, data=data)
    print(event)
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=3000)
