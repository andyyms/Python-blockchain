import datetime
import json

transaction = [{'timestamp': datetime.date(2020, 6, 28),
                'transactions': {},
                'previousHash': '0',
                'hash': '1d99923ff98052dfb064da0a8f2ef230613a4287e3cb13ecd27e7bb282560bda',
                'nonce': 0}]


res = json.dumps(transaction, indent=4, sort_keys=True, default=str)

print(res)