from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Food:
    def __init__(self, id, barcode,):
        pass



@app.route("/")
def index():
    main = "<h1>Home</h1>"
    return main












if __name__ == "__main__":
    app.run(debug=True, port=5000)