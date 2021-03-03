import json
import hashlib

# function to parse DID from public key
def didFromPK(pubKey):
    did = "did:vtn:trustid:" + str(hashlib.sha256(pubKey).hexdigest())
    return did

def didFromWallet(did_wallet_path):
    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        did = temp_did[0]['did']
    return did