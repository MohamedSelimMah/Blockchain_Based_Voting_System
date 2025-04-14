from flask import Flask,request,jsonify
from blockchain import Blockchain
app = Flask(__name__)
blockchain=Blockchain()
@app.route('/')
def index():
    return 'Blockchain voting API is working!'

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    voterId = data.get('voterId')
    