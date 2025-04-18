from flask import Flask, request, jsonify
from Blockchain.blockchain import Blockchain
import hashlib
from Utils.encryption import encrypt, decrypt
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
blockchain = Blockchain()
voted_ids = set()
registered_voters = set()

ADMIN_KEY = os.getenv("ADMIN_KEY", "default-secret-key")
MINER_REWARD_ADDRESS = "miner-reward-address"

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-Admin-Key") != ADMIN_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return wrapper

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

    with open("temp_vote.txt", "w") as f:
        f.write(vote)

    encrypted_file = f"{voter_hash}_vote_encrypted.txt"
    key, iv = encrypt("temp_vote.txt", encrypted_file)
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
        amount=1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    return jsonify({
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }), 200

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

@app.route('/admin/results', methods=['GET'])
@admin_required
def results():
    vote_counts = {}
    ADMIN_AES_KEY = os.getenv("ADMIN_AES_KEY", "default-secret-key")
    ADMIN_IV = os.getenv("ADMIN_IV", "default-secret-key")

    for block in blockchain.chain:
        for tx in block['transactions']:
            if tx['sender'] == 'network':
                continue
            encrypted_file = tx['recipient']
            try:
                decrypt(
                    key=ADMIN_AES_KEY,
                    iv=ADMIN_IV,
                    input_file=encrypted_file,
                    output_file="temp_decrypted.txt"
                )
                with open("temp_decrypted.txt", "r") as f:
                    vote = f.read().strip()
                vote_counts[vote] = vote_counts.get(vote, 0) + 1
                os.remove("temp_decrypted.txt")
            except Exception as e:
                print(f"Decryption failed for {encrypted_file}: {e}")

    return jsonify({"results": vote_counts}), 200

@app.route('/admin/decrypt', methods=['GET'])
@admin_required
def admin_decrypt():
    filename = request.args.get('file')

    if not filename or not filename.endswith('_vote_encrypted.txt'):
        return jsonify({'error': 'Invalid or missing file name'}), 400

    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        decrypt(
            key=os.getenv("ADMIN_AES_KEY", "default-secret-key"),
            iv=os.getenv("ADMIN_IV", "default-secret-key"),
            input_file=filepath,
            output_file="temp_admin_decrypted.txt"
        )
        with open("temp_admin_decrypted.txt", "r") as f:
            vote = f.read().strip()
        os.remove("temp_admin_decrypted.txt")
        return jsonify({'decrypted_vote': vote}), 200
    except Exception as e:
        return jsonify({'error': f"Decryption failed: {str(e)}"}), 500

@app.route('/')
def home():
    return "Blockchain Voting System - Endpoints: /vote, /mine, /chain, /register, /admin/*"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
