import json
import hashlib

# function to parse DID from public key
def didFromPK(pubKey):
    did = "did:vtn:trustid:" + str(hashlib.sha256(pubKey).hexdigest())
    return did