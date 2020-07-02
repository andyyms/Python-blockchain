import ecdsa
import binascii
import hashlib
import json

class Transaction:
    def __init__(self, sender_address, sender_private_key, recipient_address, amount):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount

    @property
    def __dict__(self):
        return {"sender_address": self.sender_address,
                "recipient_address": self.recipient_address,
                "amount": self.amount}


    def sign_transaction(self):
        bytes_key = binascii.unhexlify(self.sender_private_key.encode('utf-8'))
        signing_key = ecdsa.SigningKey.from_string(bytes_key,
                                                   curve=ecdsa.SECP256k1,
                                                   hashfunc=hashlib.sha256)

        signature = signing_key.sign(json.dumps(self.__dict__,
                                                indent=4).encode('utf-8'))

        return binascii.hexlify(signature)







