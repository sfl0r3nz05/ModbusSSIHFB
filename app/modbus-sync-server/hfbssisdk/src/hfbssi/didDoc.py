import json
import ecdsa
import codecs
import base64
import socket
import asyncio
import hashlib
import binascii

def createDidDocClient(path_priv_key, did_wallet_path, wallet_DidDoc, issuer):

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
        pubKeyBase64 = base64.b64encode(pem, altchars=None)
        ipaddress = socket.gethostbyname(socket.gethostname())
        issuer = issuer
        signature = ""
        countersignature = ""
        diddoc = {"context": "https://www.w3.org/ns/did/v1", "did": message.get('did'), "authentication": [{ "id": "did:vtn:trustid:4981f7c8f152f14d009c1b69d4972c84fdb4985055dc33d4d25c821ab015ad7e#keys-1", "type": "Ed25519VerificationKey2018", "issuer": issuer, "publicKeyBase58": pubKeyBase64.decode("utf-8")}],"service": [{ "id": "did:example:123456789abcdefghi#vcs", "type": "VerifiableCredentialService", "serviceEndpoint": "mbaps://{}:port".format(ipaddress),}], "signature": signature, "countersignature": countersignature}
        temp.append(diddoc)
        
    with open(wallet_DidDoc, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)
    ######################################################################


def createDidDocServer(path_priv_key, did_wallet_path, wallet_DidDoc, issuer, port, fnc, address, offset, generator, plainNumber):

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
        pubKeyBase64 = base64.b64encode(pem, altchars=None)
        ipaddress = socket.gethostbyname(socket.gethostname())
        issuer = issuer
        signature = ""
        countersignature = ""
        diddoc = {"context": "https://www.w3.org/ns/did/v1", "did": message.get('did'), "authentication": [{ "id": "did:vtn:trustid:4981f7c8f152f14d009c1b69d4972c84fdb4985055dc33d4d25c821ab015ad7e#keys-1", "type": "Ed25519VerificationKey2018", "issuer": issuer, "publicKeyBase58": pubKeyBase64.decode("utf-8")}],"service": [{ "id": "did:example:123456789abcdefghi#vcs", "type": "VerifiableCredentialService", "serviceEndpoint": "mbaps://{}:{}".format(ipaddress, port), "functionCode": fnc, "startingAddress": address, "offset": offset, "generator": generator, "plainNumber": plainNumber,}], "signature": signature, "countersignature": countersignature}
        temp.append(diddoc)
        
    with open(wallet_DidDoc, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)
    ######################################################################

def adminSignature(path_priv_key, wallet_DidDoc):
    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = ecdsa.SigningKey.from_pem(ec_priv_file.read())
    with open(wallet_DidDoc) as wallet_file:
        data = json.load(wallet_file)
        temp = data['diddoc'][0]
        h = hashlib.sha256()
        h.update((str(temp)).encode("utf-8"))
        msg_sha256_hash = h.digest()
        dataToStr = json.dumps(temp)
        dataToSign = str.encode(dataToStr)
        signature_coded = priv_eckey.sign_digest(msg_sha256_hash,sigencode=ecdsa.util.sigencode_der,)
        signature_codedBase64 = base64.b64encode(signature_coded)
        signature = str(signature_codedBase64)
        signature = signature.replace("b'", "")
        signature = signature.replace("'", "")
        data['diddoc'][0]["signature"] = signature
    with open(wallet_DidDoc, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)

def counterSignature(path_priv_key, wallet_DidDoc):
    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = ecdsa.SigningKey.from_pem(ec_priv_file.read())
    with open(wallet_DidDoc) as wallet_file:
        data = json.load(wallet_file)
        temp = data['diddoc'][0]
        h = hashlib.sha256()
        h.update((str(temp)).encode("utf-8"))
        msg_sha256_hash = h.digest()
        dataToStr = json.dumps(temp)
        dataToSign = str.encode(dataToStr)
        countersignature_coded = priv_eckey.sign_digest(msg_sha256_hash,sigencode=ecdsa.util.sigencode_der,)
        countersignature_codedBase64 = base64.b64encode(countersignature_coded)
        countersignature = str(countersignature_codedBase64)
        countersignature = countersignature.replace("b'", "")
        countersignature = countersignature.replace("'", "")
        data['diddoc'][0]["countersignature"] = countersignature
    with open(wallet_DidDoc, 'w') as wallet_file:
        json.dump(data, wallet_file, indent=4)