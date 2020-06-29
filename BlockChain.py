from Block import *
from Transaction import *
from datetime import date
from uuid import uuid4
from flask import Flask, request
import requests
import ecdsa
import binascii
import hashlib
import json
import logging

MINING_DIFFICULTY = 2
MINING_REWARD = 1

class BlockChain:
    def __init__(self):
        self.chain = [self.genesisBlock()]
        self.transactions = []
        # self.nodes = set()
        # # Generate random number to be used as node_id
        # self.node_id = str(uuid4()).replace('-', '')
        # # Create genesis block

    def last_chain(self):
        return self.chain[-1]

    def genesisBlock(self):
        return Block(date.today(), {}, "0")


    def add_block(self):
        pass

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
        transaction = Transaction(sender_address, )



    def verify_transaction_signature(self, sender_address, signature, transaction):
        return sender_address.verify(signature, json.dumps(transaction,
                                                           indent=4).encode('utf-8'), hashfunc=hashlib.sha256)


    def mine(self):
        pass




app = Flask(__name__)
blockchain = BlockChain()


@app.route('/chain', methods=["GET"])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
        print(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data},
                      indent=4,
                      default=str)

app.run(debug=True, port=5000)
