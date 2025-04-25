import hashlib
import os
from functools import wraps
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

from Blockchain.blockchain import Blockchain
from Utils.encryption import encrypt, decrypt

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RS_Group'
blockchain = Blockchain()
voted_ids = set()
registered_voters = set()
users = {}
ADMIN_KEY = os.getenv("ADMIN_KEY", "default-secret-key")
ADMIN_AES_KEY = os.getenv("ADMIN_AES_KEY", "default-secret-key")
ADMIN_IV = os.getenv("ADMIN_IV", "default-secret-key")
MINER_REWARD_ADDRESS = "miner-reward-address"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired!'}), 403
        except:
            return jsonify({'error': 'Token invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-Admin-Key") != ADMIN_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return wrapper

@app.route('/vote', methods=['POST'])
@token_required
def vote():
    data = request.get_json()
    vote = data.get('vote')
    voterId = request.user.get('username')

    if not voterId or not vote:
        return jsonify({'error': 'voterId and vote are required'}), 400

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

@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if username in users:
        return jsonify({'error': 'User already exists!'}), 400

    users[username] = generate_password_hash(password)
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({'error': 'Invalid Credentials!'}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200

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
@token_required
def register():
    voterId = request.user.get('username')

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
            key=bytes.fromhex(ADMIN_AES_KEY),
            iv=bytes.fromhex(ADMIN_IV),
            input_file=filename,
            output_file="temp_admin_decrypted.txt"
        )
        with open("temp_admin_decrypted.txt", "r") as f:
            vote = f.read().strip()
        os.remove("temp_admin_decrypted.txt")
        return jsonify({'decrypted_vote': vote}), 200
    except Exception as e:
        return jsonify({'error': f"Decryption failed: {str(e)}"}), 500

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return jsonify({'error': 'Please Provide a list of node URLs'}), 400

    for node in nodes:
        parsed_url = urlparse(node)
        if parsed_url.netloc:
            blockchain.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            blockchain.nodes.add(parsed_url.path)
        else:
            return jsonify({'error': f'Invalid Node URL: {node}'}), 400
    return jsonify({
        'message': 'New nodes added',
        'total_nodes': list(blockchain.nodes),
    }), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        return jsonify({
            'message': 'Chain was replaced with a longer valid chain.',
            'new_chain': blockchain.chain
        }), 200
    else:
        return jsonify({
            'message': 'Our chain is authoritative.',
            'chain': blockchain.chain
        }), 200

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/vote', methods=['GET'])
def vote_page():
    return render_template('vote.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/result', methods=['GET'])
@admin_required
def results_page():
    return render_template("results.html")
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
