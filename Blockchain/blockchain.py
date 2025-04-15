import hashlib
from time import time
import json

class Blockchain:
    def __init__(self):
        self.current_transactions =[]
        self.chain = []
        self.nodes = set()

        self.new_block(proof='100',previous_hash='1')

    def new_block(self,proof,previous_hash= None):
        block={
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def current_transactions(self,sender,amount,recipient):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index']+1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block , sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self,last_proof):
        proof=0
        while self.valid_proof(last_proof,proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof,proof):
        g=f'{last_proof}{proof}'.encode()
        g_hash=hashlib.sha256(g).hexdigest()
        return g_hash[:4] == "0000"


