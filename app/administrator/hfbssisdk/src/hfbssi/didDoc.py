import codecs
import base64
import socket


def createDidDocClient(path_priv_key, did_wallet_path, wallet_DidDoc):

    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = ecdsa.SigningKey.from_pem(ec_priv_file.read())

    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        message = temp_did[0]

    # Writing the keys on the wallet #####################################
    with open(wallet_DidDoc) as wallet_file:
        data = json.load(wallet_file)
        temp = data['diddoc']
        pem = priv_eckey.get_verifying_key().to_pem()
        publicKey = pem.decode("utf-8")
        pubKeyBase64 = base64.b64encode(publicKey, altchars=None)
        ipaddress = socket.gethostbyname(socket.gethostname())
        diddoc = {"@context": "https://www.w3.org/ns/did/v1", "did": message.get('did'), "authentication": [{"id": "did:vtn:trustid:4981f7c8f152f14d009c1b69d4972c84fdb4985055dc33d4d25c821ab015ad7e#keys-1", "type": "Ed25519VerificationKey2018", "issuer": issuer, "publicKeyBase58": pubKeyBase64]}, "service": [{"id": "did:example:123456789abcdefghi#vcs", "type": "VerifiableCredentialService", "serviceEndpoint": "mbaps://{}:port".format(ipaddress)}], "signature": signature, "countersign": countersign}
        temp.append(diddoc)
        
    with open(wallet_DidDoc, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)
    ######################################################################
