import os
import base64
import socket
import hashlib
import asyncio
from hfc.fabric import Client
from hfc.fabric_ca.caservice import ca_service
from hfc.fabric_network import wallet


def invokeSyncClient():
    loop = asyncio.get_event_loop()
    cli = Client(
        net_profile="../connection-profile/2org_2peer_solo/network.json")
    user1 = cli.get_user('org1.example.com', 'User1')

    cli.new_channel('modbuschannel')
    gopath_bak = os.environ.get('GOPATH', '')
    gopath = os.path.normpath(os.path.join(
        os.path.dirname(os.path.realpath('__file__')),
        '../chaincode'
    ))
    os.environ['GOPATH'] = os.path.abspath(gopath)

    host_ip = socket.gethostbyname(socket.gethostname())
    name = host_ip.encode("utf-8")
    arg2 = base64.b64encode(hashlib.sha256(name).digest())
    args = ["client", arg2]
    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
        requestor=user1,
        channel_name='modbuschannel',
        peers=['peer0.org1.example.com'],
        args=args,
        cc_name='registration_cc_v2',
        transient_map=None,  # optional, for private data
        # for being sure chaincode invocation has been commited in the ledger, default is on tx event
        wait_for_event=True,
        # cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
    ))
