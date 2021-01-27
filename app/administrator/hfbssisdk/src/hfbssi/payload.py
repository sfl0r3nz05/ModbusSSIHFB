# generate payload to insert key value pair
import json
import codecs
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from jwt.utils import base64url_decode, force_bytes, force_unicode
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key)


def payloadgen(path_priv_key, did_wallet_path):
    with open(key_wallet_path) as wallet_file:
        data = json.load(wallet_file)
        temp_key = data['keys']
        PRIVATE_KEY = temp_key[0].get('privKey')
        PRIVATE_KEY_ENC = bytes(PRIVATE_KEY.encode('utf-8'))
        print(PRIVATE_KEY_ENC)
        # RSA_SERIALIZATION = codecs.decode(
        #    PRIVATE_KEY_ENC, encoding='utf-8', errors='strict')
        RSA_SERIALIZATION = serialization.load_pem_private_key(
            PRIVATE_KEY_ENC, password=None, backend=default_backend())

    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        message = temp_did[0]

    return temp_did.did, signature
