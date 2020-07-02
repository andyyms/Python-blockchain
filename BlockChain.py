from Block import *
from Transaction import *
from datetime import date
from uuid import uuid4
from flask import Flask, render_template, jsonify, request
import hashlib
import json
import logging

MINING_SENDER = "ANDY YEUNG"
MINING_DIFFICULTY = 2
MINING_REWARD = 1

class BlockChain:
    def __init__(self):
        self.chain = [self.genesisBlock()]
        self.transactions = []
        self.nodes = set()
        # Generate random number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')

    @property
    def last_block(self):
        return self.chain[-1]

    def genesisBlock(self):
        return Block(date.today(), {}, "0")


    def add_block(self, block, proof):
        if block.previousHash != self.last_block.hash:
            return False

        if not self.is_valid_chain(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * MINING_DIFFICULTY)) and \
                block_hash == block.calculateHash()

    def proof_of_work(self):
        block = self.chain[-1]
        computed_hash = str(block.calculateHash())

        while not computed_hash.startWith('0' * MINING_DIFFICULTY):
            block.nonce += 1
            computed_hash = block.calculateHash()
        return computed_hash


    def verify_transaction(self, sender_priKey, signature, transaction):
        return sender_priKey.verify(signature,
                             json.dumps(transaction, indent=4).encode('utf-8'),
                             hashfunc=hashlib.sha256)


    def getBalanceOfAddress(self, address):
        balance = 0
        chain = self.chain

        for block in chain:
            for transactions in block:
                for tran in transactions:
                    if tran.sender_Address == address:
                        balance -= tran.amount
                    if tran.recipient_address == address:
                        balance += tran.amount
        return balance

    def is_valid_chain(self):
        chain = self.chain
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]

            if current_block.previousHash != previous_block.hash:
                logging.info('Some block\'s previous hash does not match to previous block\'s hash.')
                return False

            if current_block.hash != current_block.calculateHash():
                logging.info('The current block has been tempered')
                return False
        return True

    def submit_transaction(self, sender_address, recipient_address, amount, signature):
        transaction = {'sender_address': sender_address,
                       'recipient_address': recipient_address,
                       'amount': amount}


        # Reward for mining a block
        if sender_address == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        # Manages transactions from wallet to another wallet
        else:
            transaction_verification = self.verify_transaction_signature(sender_address, signature, transaction)
            if transaction_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
            else:
                return False



    def verify_transaction_signature(self, sender_address, signature, transaction):
        publicKeyVerifyObject = ecdsa.VerifyingKey.from_string(
                                            bytes.fromhex(sender_address),
                                            curve=ecdsa.SECP256k1,
                                            hashfunc=hashlib.sha256)

        # print(f'sender_address: {sender_address}')
        # print(f'signature: {signature}')
        # print(f'transaction: {json.dumps(transaction, indent=4)}')

        is_valid = publicKeyVerifyObject.verify(bytes.fromhex(signature),
                                            json.dumps(transaction, indent=4).encode('utf-8'),
                                            hashfunc=hashlib.sha256)

        # print(f'is_valid: {is_valid}')

        return is_valid


    def mine(self):
        # Stop mining if no pending transaction
        if not self.transactions:
            return False

        last_block = self.last_block

        new_block = Block(timestamp=time(),
                          transactions=self.transactions,
                          previousHash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.transactions = []


app = Flask(__name__)
blockchain = BlockChain()

@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/chain', methods=["GET"])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    data = json.dumps({"length": len(chain_data),
                       "chain": chain_data},
                      indent=4,
                      default=str)

    print(json.dumps(blockchain.transactions, indent=4))

    return data

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                            hashfunc=hashlib.sha256)
    public_key = signing_key.get_verifying_key()

    response = {
        'private_key': binascii.hexlify((signing_key.to_string())).decode('utf-8'),
        'public_key': binascii.hexlify((public_key.to_string())).decode('utf-8')
    }
    return jsonify(response), 200


@app.route('/make/transaction')
def make_transaction():
    return render_template('./make_transaction.html')


@app.route('/view/transactions')
def view_transactions():
    return render_template('./view_transactions.html')


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_address = request.form['sender_address']
    sender_private_key = request.form['sender_private_key']
    recipient_address = request.form['recipient_address']
    value = request.form['amount']

    transaction = Transaction(sender_address, sender_private_key, recipient_address, value)

    response = {'transaction': {'sender_address': transaction.sender_address,
                                'amount': transaction.amount,
                                'recipient_address': transaction.recipient_address},
                'signature': transaction.sign_transaction().decode('utf-8')}


    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['sender_address', 'recipient_address', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    transaction_result = blockchain.submit_transaction(values['sender_address'],
                                                       values['recipient_address'],
                                                       values['amount'],
                                                       values['signature'])

    if transaction_result == False:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406
    else:
        response = {'message': 'Transaction will be added to Block ' + str(transaction_result)}
        return jsonify(response), 201



app.run(debug=True, port=5000)