
# generateDID generates a new DID in the wallet
import json
import hashlib


# function to generate DID
def generateDID(wallet, controller, pathpubKey, pathprivKey):
    with open(wallet) as wallet_file:
        data = json.load(wallet_file)
        temp = data['dids']
        with open(pathprivKey) as f:
            privKey = f.read()
            privKey = privKey.replace('\n', '')
        with open(pathpubKey) as f:
            pubKey = f.read()
            pubKey = pubKey.replace('\n', '')
        did = "did:vtn:trustid:" + \
            str(hashlib.sha256(pubKey.encode('utf-8')).hexdigest())
        y = {
            "did": did,
            "controller": controller,
            "pubKey": pubKey,
            "privKey": privKey
        }
        temp.append(y)
    with open(wallet, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)
