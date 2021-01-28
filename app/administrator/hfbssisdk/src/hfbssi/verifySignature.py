import json
import codecs
import hashlib
import sys
import os
import platform
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography import x509
import cryptography
from cryptography.hazmat.primitives.asymmetric import padding


def verifySignature(pem, did_wallet_path):

    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        dictDid = temp_did[0]
        signature = dictDid.get('signature')
        did = dictDid.get('did')

        strToDic = json.loads(pem)

        parsed_pem = strToDic.get('publicKey')

        pemToBytes = str.encode(parsed_pem)

        loaded_public_key = serialization.load_pem_public_key(
            pemToBytes, backend=default_backend())

        response = isinstance(loaded_public_key, ec.EllipticCurvePublicKey)

        if response:
            try:

                # Original signature coded str to hex
                signatureToBytes = signature.encode('utf-8')

                # Signature decode hex to bytes
                signature_decoded = codecs.decode(
                    signatureToBytes, encoding='hex_codec', errors='strict')

                # Encode did identifier
                didToBytes = did.encode('utf-8')

                # Compute the signature verification
                loaded_public_key.verify(
                    signature_decoded, didToBytes, signature_algorithm=ec.ECDSA(hashes.SHA256()))

                return True

            except ValueError:
                return 0
