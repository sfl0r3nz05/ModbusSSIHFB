import os
import json
import ecdsa
import codecs
import asyncio
import hashlib
from hfc.fabric import Client
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key)


def payloadToRegisterDid(path_priv_key, did_wallet_path):

    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = ecdsa.SigningKey.from_pem(ec_priv_file.read())

    with open(did_wallet_path) as did_file:
        data = json.load(did_file)
        temp_did = data['dids']
        message = temp_did[0]

        pem = priv_eckey.get_verifying_key().to_pem()
        input = json.dumps({
            "did": message.get('did'),
            "publicKey": pem.decode("utf-8"),
        })
        return input


def registerDid(net_profile, organization, user, channel, peer, chaincode, function, arg0):
    loop = asyncio.get_event_loop()
    cli = Client(net_profile=net_profile)
    org1_admin = cli.get_user(organization, user)
    cli.new_channel(channel)
    gopath = os.path.normpath(os.path.join(os.path.dirname(
        os.path.realpath('__file__')), '../chaincode'))
    os.environ['GOPATH'] = os.path.abspath(gopath)

    args = [arg0]
    loop.run_until_complete(cli.chaincode_invoke(
        requestor=org1_admin,
        channel_name=channel,
        peers=[peer],
        args=args,
        cc_name=chaincode,
        transient_map=None,  # optional, for private data
        wait_for_event=True,
        fcn=function,
    ))
