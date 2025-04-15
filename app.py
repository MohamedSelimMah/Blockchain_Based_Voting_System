from flask import Flask,request,jsonify
from blockchain import Blockchain
import hashlib
app = Flask(__name__)
blockchain=Blockchain()
voted_ids = set()

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    voterId = data.get('voterId')
    vote = data.get('vote')
    voter_hash = hashlib.sha256(voterId.encode()).hexdigest()

    if voter_hash in voted_ids:
        return jsonify({'message': 'You have already voted!'}), 400

    blockchain.current_transactions.append({'voter': voter_hash, 'vote': vote})
    voted_ids.add(voter_hash)

    return jsonify({'message': 'Vote successfully recorded.'}), 200
