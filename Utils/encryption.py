import os
from Cryptodome.Cipher import AES
import requests
from future.backports.urllib.parse import urlparse


def pad(data):
    padding_length = 16 - len(data)%16
    padding = bytes([padding_length]* padding_length)
    return  data + padding

def unpad(data):
    padding_length = data[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Padding is Invalid")
    return data[:-padding_length]

def encrypt(input_file, output_file):
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        with open(input_file, 'rb') as f:
            plaintext = f.read()

        padded_plaintext = pad(plaintext)
        ciphertext = cipher.encrypt(padded_plaintext)

        with open(output_file, 'wb') as f:
            f.write(iv + ciphertext)

        return key.hex(), iv.hex()
    except Exception as e:
        print(f"An error occurred during encryption: {str(e)}")
        return None, None

def decrypt(key, iv, input_file, output_file):
    try:
        decoded_key = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(iv)

        if len(decoded_key) != 32:
            raise ValueError("Invalid AES key length")

        cipher = AES.new(decoded_key, AES.MODE_CBC, iv_bytes)

        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        ciphertext = encrypted_data[16:]
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

    except Exception as e:
        print(f"Decryption error: {str(e)}")

def register_node(self,address):
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)

def valid_chain(self,chain):
    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
        block = chain[current_index]
        if block['previous_hash'] != last_block(last_block):
            return False
        if not self.valid_proof(last_block['proof'],block['proof']):
            return False
        last_block = block
        current_index += 1
    return True

def resolve_conflicts(self):
    neighbours = self.nodes
    new_chain = None
    max_len = len(self.chain)

    for node in neighbours:
        try:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_len and self.valid_proof(chain):
                    max_len = length
                    new_chain = chain
        except Exception as e:
            print(f"Failed to connect to {node}: {e}")

        if new_chain:
            self.chain = new_chain
            return True
    return False