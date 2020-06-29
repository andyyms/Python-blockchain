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


    def sign_transaction(self):
        bytes_key = binascii.unhexlify(self.sender_private_key)
        signing_key = ecdsa.SigningKey.from_string(bytes_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
        # signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)

        signature = signing_key.sign(json.dumps(self.__dict__,
                                                indent=4).encode())
        return signature


my_pri_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
my_pub_key = my_pri_key.get_verifying_key()

print(f'my_pri_key: {my_pri_key} and my_pub_key: {my_pub_key}')

tran = Transaction(my_pub_key)







