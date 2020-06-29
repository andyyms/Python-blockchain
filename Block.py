import hashlib
import json
from time import *
from Transaction import *

class Block:
    def __init__(self, timestamp, transactions, previousHash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()


    def calculateHash(self):
        return hashlib.sha256(json.dumps(self.__dict__).encode()).hexdigest()

    def __repr__(self):
        return json.dumps({'timestamp': self.timestamp,
                           'transaction': self.transactions,
                           'hash': self.hash,
                           'previousHash': self.previousHash,
                           'nonce': self.nonce})

    def proof_of_work(self):
        computed_hash = str(self.calculateHash())

        while not computed_hash.startswith('0' * 3):
            block.nonce += 1
            computed_hash = self.calculateHash()
        return computed_hash


block = Block(time(),
              {'fromAddress': 'Andy',
               'toAddress': 'Betty',
               'amount': 100},
              "0")


print(block.proof_of_work())


# print(hashlib.sha256(json.dumps(block.__dict__).encode()).hexdigest())




