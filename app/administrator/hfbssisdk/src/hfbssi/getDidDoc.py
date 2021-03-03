import os
import json
import ecdsa
import codecs
import base64
import asyncio
import hashlib
import binascii
from hfc.fabric import Client
from asn1crypto.core import Sequence
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key)


def payloadToDidDoc(path_priv_key, did_wallet_path, method, entityDid):

    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = ecdsa.SigningKey.from_pem(ec_priv_file.read())

    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        message = temp_did[0]

        pem = priv_eckey.get_verifying_key().to_pem()

        msg = {"method": method,"params": {"did": entityDid,}, "hash": "", "signature": "",}

        h = hashlib.sha256()
        h.update((str(msg)).encode("utf-8"))
        msg_sha256_hash = h.digest()
        dataToStr = json.dumps(msg)
        dataToSign = str.encode(dataToStr)
        signature_coded = priv_eckey.sign_digest(msg_sha256_hash,sigencode=ecdsa.util.sigencode_der,)

        msgNew = {"method": method, "params": {"did": entityDid}, "hash": base64.b64encode(msg_sha256_hash), "signature": base64.b64encode(signature_coded)}
        msgNewP1 = (str(msgNew)).replace("b'", "'")
        msgNewP2 = msgNewP1.replace("'", '"')
        b64hash = base64.b64encode(msgNewP2.encode('utf-8'))
        input = json.dumps({
            "did": message.get('did'),
            "payload": b64hash.decode("utf-8"),
        })
        return input

def requestDidDoc(net_profile, organization, user, channel, peer, chaincode, function, arg0):
    loop = asyncio.get_event_loop()
    cli = Client(net_profile=net_profile)
    org1_admin = cli.get_user(organization, user)
    cli.new_channel(channel)
    gopath = os.path.normpath(os.path.join(os.path.dirname(
        os.path.realpath('__file__')), '../chaincode'))
    os.environ['GOPATH'] = os.path.abspath(gopath)

    args = [arg0]
    response = loop.run_until_complete(cli.chaincode_invoke(
        requestor=org1_admin,
        channel_name=channel,
        peers=[peer],
        args=args,
        cc_name=chaincode,
        transient_map=None,
        wait_for_event=True,
        fcn=function,
    ))
    return response