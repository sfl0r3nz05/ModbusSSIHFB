import codecs
import base64
import socket


def didDocServer(did, pubKey, controller, port, fnc, address, offset):

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
            "serviceEndpoint": "mbaps://{}:{}".format(ipaddress, port),
            "functionCode": fnc,
            "startingAddress": address,
            "offset": offset,
        }]
    }

    return diddoc


def didDocServerSigned(diddocserver, signatureserver):

    # Parsing data type from bytes to hex
    signature_coded = codecs.encode(
        signatureserver, encoding='hex_codec', errors='strict')

    # Parsing data type from bytes to hex
    diddocserver['issuerSignature'] = signature_coded.decode('utf-8')

    return diddocserver
