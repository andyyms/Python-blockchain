import ecdsa
import binascii
import hashlib
import json


signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
public_key = signing_key.get_verifying_key()

publicKeyVerifyObject = ecdsa.VerifyingKey.from_string(bytes.fromhex(binascii.hexlify(public_key.to_string()).decode('utf-8')),
                                                       curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)

msg = 'I am boy'.encode('utf-8')
sig = signing_key.sign(msg)


print("private key: ", binascii.hexlify((signing_key.to_string())))
print("public key:", binascii.hexlify(publicKeyVerifyObject.to_string()))
print("signature: ", binascii.hexlify(sig))

isValid = publicKeyVerifyObject.verify(sig, msg, hashfunc=hashlib.sha256)

print(isValid)



# publicKeyVerifyObject = ecdsa.VerifyingKey.from_string(bytes.fromhex(binascii.hexlify(public_key.to_string()).decode('utf-8')),
#                                                        curve=ecdsa.SECP256k1,
#                                                        hashfunc=hashlib.sha256)

# print(f'private key: {binascii.hexlify((signing_key.to_string()))}')
# print()
# print(type(binascii.hexlify(public_key.to_string()).decode('utf-8')))
# print()
# print("public key:", binascii.hexlify(public_key.to_string()))
# print("public key:", binascii.hexlify(publicKeyVerifyObject.to_string()))





# # a message to sign
# transaction = json.dumps({"sender_address": "Andy Yeung",
#                               "receipent": "Fanny Leung",
#                               "amount": "10"},
#                          indent=4).encode('utf-8')
#
# # signature of the message
# signature = signing_key.sign(transaction)
#
# print()
# print(signature)
# print()
# print(f'signature: {binascii.hexlify(signature)}')
#
# is_valid = public_key.verify(signature, transaction, hashfunc=hashlib.sha256)
#
# print(f'is_valid: {is_valid}')
#
#
#
# # Test Program
# try:
#     print(publicKeyVerifyObject.verify(signature, transaction))
# except ecdsa.BadSignatureError:
#     print(False)
#
#
# try:
#     print(public_key.verify(signature, transaction))
# except ecdsa.BadSignatureError:
#     print(False)

