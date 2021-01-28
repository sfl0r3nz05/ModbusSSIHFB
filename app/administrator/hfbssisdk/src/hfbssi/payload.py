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

    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = load_pem_private_key(force_bytes(
            ec_priv_file.read()), password=None, backend=default_backend())

    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        message = temp_did[0]

        if message.get('controller'):
            # to convert dictionary into string using json.dumps() https://www.geeksforgeeks.org/python-convert-dictionary-object-into-string/
            dataToStr = json.dumps(message)

            # Use client/server DID as message to be signed
            dataToSign = str.encode(dataToStr)

            # signing message https://github.com/pyca/cryptography/blob/master/docs/hazmat/primitives/asymmetric/ec.rst
            signature_coded = priv_eckey.sign(
                dataToSign, ec.ECDSA(hashes.SHA256()))

            #signature = signature_coded.decode("utf-8")
            signature = signature_coded.decode(
                'unicode_escape').encode('utf-8')

            return message.get('did'), signature

        else:
            public_key = priv_eckey.public_key()
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
            # pem.splitlines()[1] //To access to different segments of the pem
            # loaded_public_key = serialization.load_pem_public_key(
            #    pem, backend=default_backend())

            return message.get('did'), pem
