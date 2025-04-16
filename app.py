from flask import Flask, request, jsonify
from Blockchain.blockchain import Blockchain
import hashlib
from Utils.encryption import encrypt
import os


app = Flask(__name__)
blockchain = Blockchain()
voted_ids = set()
registered_voters = set()

MINER_REWARD_ADDRESS = "miner-reward-address"

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    voterId = data.get('voterId')
    vote = data.get('vote')
    voter_hash = hashlib.sha256(voterId.encode()).hexdigest()
    if voter_hash not in registered_voters:
        return jsonify({'error': 'Voter not registered'}), 403
    if voter_hash in voted_ids:
        return jsonify({'message': 'You have already voted!'}), 400

    with open("temp_vote.txt","w") as f:
        f.write(vote)

    encrypted_file = f"{voter_hash}_vote_encrypted.txt"
    key,iv = encrypt("temp_vote.txt",encrypted_file)
    os.remove("temp_vote.txt")

    if not key:
        return jsonify({'message': 'Encryption Failed'}), 400

    blockchain.add_transaction(
        sender=voter_hash,
        recipient=encrypted_file,
        amount=1
    )
    voted_ids.add(voter_hash)

    return jsonify({'message': 'Vote successfully recorded.'}), 200

@app.route('/mine', methods=['GET'])
def mine():
    if not blockchain.transactions:
        return jsonify({'message': 'No transactions to mine'}), 400

    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)

    blockchain.add_transaction(
        sender="network",
        recipient=MINER_REWARD_ADDRESS,
        amount=1  # Mining reward
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    voterId = data.get('voterId')

    if not voterId:
        return jsonify({'error': 'Voter ID is required'}), 400

    voter_hash = hashlib.sha256(voterId.encode()).hexdigest()

    if voter_hash in registered_voters:
        return jsonify({'error': 'Voter already registered'}), 400

    registered_voters.add(voter_hash)
    return jsonify({'message': 'Voter registered successfully', 'voter_hash': voter_hash}), 200

@app.route('/admin/register', methods=['GET'])
def list_voters():
    return jsonify({'voters': list(registered_voters)}), 200

@app.route('/')
def home():
    return "Blockchain Voting System - Endpoints: /vote (POST), /mine (GET), /chain (GET)"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

