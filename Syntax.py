import ecdsa
import binascii
import hashlib
import json


# private_key = b'f180f3a2b5cf866e4566b1613b0605070f8f219792fb61df6cba441e4411beca'
# public_key = b'5296f32bf9680225b80692381edfaa2502bbb3774f6a0d5b1469ba01f4c9a4c28a9ffbc15588ebae210b7be7ba50a1cb6f0e91153bfec4fd9c8b3466cfc0f406'
# signature = b'f38325527de0aec9dc20301ea4b21cb7ef2c26f8418b26b34755e31f7fcb17deb2418730fe9f1da1af0fce46c5f4a1aec6a79ea691546a671f86fcec7bb38d21'
#
#
# vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key.decode('utf-8')),
#                                     curve=ecdsa.SECP256k1,
#                                     hashfunc=hashlib.sha256)
#
# message = 'I am boy'.encode('utf-8')
#
#
# is_valid = vk.verify(bytes.fromhex(signature.decode('utf-8')), message, hashfunc=hashlib.sha256)
#
# print(f'is_valid: {is_valid}')




private_key = '695eeddd5d5e6b7f052fb14f55c6baf45c54307ba7661eb18dbd738b83257c63'
public_key = '78f348919a65df91319c521d7bf0dce98509595f09660bc069c411970e63febd3be6fcd110d506b7d3368488462089222fbbb126f90168d04ad0a767e64f7e2c'
signature = '44df1ad3e95300847e01e3b506d36e1d49c12891460d6b31dc642f418e6a8f84b849a1bf477567dbcf2287b54a998485ccf81848c4b7e08476338261b3387313'

vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key),
                                    curve=ecdsa.SECP256k1,
                                    hashfunc=hashlib.sha256)


sender = "78f348919a65df91319c521d7bf0dce98509595f09660bc069c411970e63febd3be6fcd110d506b7d3368488462089222fbbb126f90168d04ad0a767e64f7e2c"
receipient = "95eb479221f814baf68b5cce7bc43b0410851a010b2b34fa1d0244f461d3a6476b1bcb3ce1b6298189fbff073e8a8a86297115e63f29bd2941c3a5c27efcda8e"


message = json.dumps({"sender_address": sender,
                        "receipient_address": receipient,
                        "amount": "100"},
                      indent=4).encode('utf-8')


message = json.dumps({
    "sender_address": "78f348919a65df91319c521d7bf0dce98509595f09660bc069c411970e63febd3be6fcd110d506b7d3368488462089222fbbb126f90168d04ad0a767e64f7e2c",
    "recipient_address": "95eb479221f814baf68b5cce7bc43b0410851a010b2b34fa1d0244f461d3a6476b1bcb3ce1b6298189fbff073e8a8a86297115e63f29bd2941c3a5c27efcda8e",
    "amount": "100"
},indent=4).encode('utf-8')

is_valid = vk.verify(bytes.fromhex(signature), message, hashfunc=hashlib.sha256)

print(f'is_valid: {is_valid}')
