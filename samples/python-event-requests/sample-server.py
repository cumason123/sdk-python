from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return "Hello World!"

@app.route('/event', methods=['POST'])
def hello():
    print(request.get_json())
    return "Hello World!"

if __name__ == '__main__':
    app.run()