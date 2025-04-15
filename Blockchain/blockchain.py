import hashlib
from time import time
import json

import requests


class Blockchain:
    def __init__(self):
        self.new_transactions =[]
        self.chain = []
        self.nodes = set()

        self.new_block(proof=100,previous_hash='1')

    def new_block(self,proof,previous_hash= None):
        block={
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions':self.new_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }
        self.new_transactions = []
        self.chain.append(block)
        return block

    def new_transactions(self,sender,amount,recipient):
        self.new_transactions.append({
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

    def valid_chain(self,chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'],block['proof']):
                return False

            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain =None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False