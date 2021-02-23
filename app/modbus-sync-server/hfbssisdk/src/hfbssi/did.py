# generateDID generates a new DID in the wallets
import json
import codecs
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from jwt.utils import force_bytes
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key)

GLOBAL_PAYLOAD = 0
GLOBAL_DID_ENTITY = 0
GLOBAL_PUB = bytearray()
GLOBAL_PRIV = bytearray()
GLOBAL_DID_CONTROLLER = 0
EC_SERIALIZATION = bytearray()


# function to administrator issues DID identifier to it self
def createDID(wallet, walletDid, pathkey):
    # Global variable to store DID and send to createDID method
    global GLOBAL_DID_CONTROLLER
    # Global variable to store private key and send to createDID method
    global GLOBAL_PRIV
    # Global variable to store public key and send to createDID method
    global GLOBAL_PUB
    # Global variable to store public key and send to createDID method
    global EC_SERIALIZATION
    # Global variable to store DID of client/server
    global GLOBAL_DID_ENTITY
    # Global variable to store payload
    global GLOBAL_PAYLOAD

    # Load admin private key https://github.com/pyca/cryptography/blob/master/docs/hazmat/primitives/asymmetric/ec.rst
    with open(pathkey, 'r') as ec_priv_file:
        priv_eckey = load_pem_private_key(force_bytes(
            ec_priv_file.read()), password=None, backend=default_backend())

    EC_SERIALIZATION = priv_eckey

    # Variables generated to create administrator DID
    # Private Key serialization without encryption: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa.html#key-serialization
    priv_key_pem = priv_eckey.private_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())

    # Parsing data type from bytes to hex
    GLOBAL_PRIV = codecs.encode(priv_key_pem, 'hex_codec')

    # Public Key serialization without encryption: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa.html#key-serialization
    public_key = priv_eckey.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # Parsing data type from bytes to hex
    GLOBAL_PUB = codecs.encode(public_key_pem, 'hex_codec')

    # Create DID identifier for administrator
    did_controller = "did:vtn:trustid:" + \
        str(hashlib.sha256(public_key_pem).hexdigest()
            )

    # GLOBAL variable to send administrator DID to createDID method
    GLOBAL_DID_CONTROLLER = did_controller

    # Writing the keys on the wallet #####################################
    with open(wallet) as wallet_file:
        data = json.load(wallet_file)
        temp = data['keys']

        y = {
            # GLOBAL variable decoded before sending to wallet
            "privKey": GLOBAL_PRIV.decode('utf-8'),
            # GLOBAL variable decoded before sending to wallet
            "pubKey": GLOBAL_PUB.decode('utf-8'),
        }
        temp.append(y)

    # Object added to Json file
    with open(wallet, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)
    ######################################################################

    # Writing the dids on the wallet #####################################
    with open(walletDid) as walletDid_file:
        data = json.load(walletDid_file)
        tempDid = data['dids']

        x = {
            # DID retrieved from GLOBAL variable
            "did": GLOBAL_DID_CONTROLLER,
            # GLOBAL variable decoded before sending to wallet
            "pubKey": GLOBAL_PUB.decode('utf-8'),
        }
        tempDid.append(x)

    # Object added to Json file
    with open(walletDid, 'w') as walletDid_file:
        json.dump(data, walletDid_file, indent=4)
    ######################################################################