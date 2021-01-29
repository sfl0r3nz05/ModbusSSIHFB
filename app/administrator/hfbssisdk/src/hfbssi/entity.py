import os
import json
import codecs
import hashlib
import asyncio
from hfc.fabric import Client
from cryptography.hazmat.primitives import hashes
from hfbssisdk.src.hfbssi.diddocclient import didDocClient
from hfbssisdk.src.hfbssi.diddocserver import didDocServer
from hfbssisdk.src.hfbssi.diddocclient import didDocClientSigned
from hfbssisdk.src.hfbssi.diddocserver import didDocServerSigned
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from jwt.utils import base64url_decode, force_bytes, force_unicode
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key)


def payloadToRegisterEntity(path_priv_key):
    # Load admin private key https://github.com/pyca/cryptography/blob/master/docs/hazmat/primitives/asymmetric/ec.rst
    with open(path_priv_key, 'r') as ec_priv_file:
        priv_eckey = load_pem_private_key(force_bytes(
            ec_priv_file.read()), password=None, backend=default_backend())

    # Public Key serialization without encryption: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa.html#key-serialization
    public_key = priv_eckey.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # Create DID identifier for administrator
    did_entity = "did:vtn:trustid:" + \
        str(hashlib.sha256(public_key_pem).hexdigest()
            )
    return did_entity, public_key_pem


def registerEntity(net_profile, organization, user, channel, peer, chaincode, function, arg1, arg2, arg3):
    loop = asyncio.get_event_loop()
    cli = Client(net_profile=net_profile)
    org1_admin = cli.get_user(organization, user)
    cli.new_channel(channel)
    gopath = os.path.normpath(os.path.join(os.path.dirname(
        os.path.realpath('__file__')), '../chaincode'))
    os.environ['GOPATH'] = os.path.abspath(gopath)

    args = [arg1, arg2, arg3]
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
