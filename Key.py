# from nacl.public import PrivateKey
# import binascii
#
# privateKey = PrivateKey.generate()
# publicKey = privateKey.public_key
#
# priKey = binascii.hexlify(bytes(privateKey))
# pubKey = binascii.hexlify(bytes(publicKey))
#
# print(f'Your private key: {binascii.hexlify(bytes(privateKey))}')
# print(f'Your public key: {binascii.hexlify(bytes(publicKey))}')


# from fastecdsa import keys, curve,ecdsa
# priv_key, pub_key = keys.gen_keypair(curve.secp256k1)
#
# print(pub_key)

import ecdsa
import binascii
import hashlib
import json


signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
public_key = signing_key.get_verifying_key()

publicKeyVerifyObject = ecdsa.VerifyingKey.from_string(bytes.fromhex(binascii.hexlify(public_key.to_string()).decode('utf-8')),
                                                       curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)

print(f'private key: {binascii.hexlify((signing_key.to_string()))}')
print("public key:", binascii.hexlify(public_key.to_string()))
print("public key:", binascii.hexlify(publicKeyVerifyObject.to_string()))

# a message to sign
name = "lastpeony"

# signature of the message
# signature = signing_key.sign(name.encode('utf-8'))
signature = signing_key.sign(json.dumps({"sender_address": "Andy Yeung",
                              "receipent": "Fanny Leung",
                              "amount": "10"},
                                        indent=4).encode())

print(f'signature: {binascii.hexlify(signature)}')

is_valid = public_key.verify(signature, json.dumps({"sender_address": "Andy Yeung",
                              "receipent": "Fanny Leung",
                              "amount": "10"},
                                        indent=4).encode('utf-8'), hashfunc=hashlib.sha256)

print(f'is_valid: {is_valid}')


# # Test Program
# try:
#     print(publicKeyVerifyObject.verify(signature, name.encode('utf-8')))
# except ecdsa.BadSignatureError:
#     print(False)
#
#
# try:
#     print(public_key.verify(signature, name.encode('utf-8')))
# except ecdsa.BadSignatureError:
#     print(False)

