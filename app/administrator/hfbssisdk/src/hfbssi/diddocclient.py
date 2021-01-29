import codecs
import base64
import socket


def didDocClient(did, pubKey, controller):

    pubKeyBase64 = base64.b64encode(pubKey, altchars=None)

    ipaddress = socket.gethostbyname(socket.gethostname())

    # DID Doc creation
    diddoc = {
        "@context": "https://www.w3.org/ns/did/v1",
        "id": did,
        "authentication": [{
            "id": "did:vtn:trustid:4981f7c8f152f14d009c1b69d4972c84fdb4985055dc33d4d25c821ab015ad7e#keys-1",
            "type": "Ed25519VerificationKey2018",
            "controller": controller,
            "publicKeyBase58": pubKeyBase64
        }],
        "service": [{
            "id": "did:example:123456789abcdefghi#vcs",
            "type": "VerifiableCredentialService",
            "serviceEndpoint": "mbaps://{}:port".format(ipaddress),
        }]
    }

    return diddoc


def didDocClientSigned(diddocclient, signatureclient):

    # Parsing data type from bytes to hex
    signature_coded = codecs.encode(
        signatureclient, encoding='hex_codec', errors='strict')

    # Parsing data type from bytes to hex
    diddocclient['issuerSignature'] = signature_coded.decode('utf-8')

    return diddocclient
