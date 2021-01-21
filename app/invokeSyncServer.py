import os
import asyncio
from hfc.fabric import Client
import hashlib
import base64
import socket


def invokeSyncServer():
    loop = asyncio.get_event_loop()
    cli = Client(
        net_profile="../connection-profile/2org_2peer_solo/network.json")
    user2 = cli.get_user('org2.example.com', 'User1')

    # Make the client know there is a channel in the network
    cli.new_channel('modbuschannel')

    # Install Example Chaincode to Peers
    # GOPATH setting is only needed to use the example chaincode inside sdk#
    gopath_bak = os.environ.get('GOPATH', '')
    gopath = os.path.normpath(os.path.join(
        os.path.dirname(os.path.realpath('__file__')),
        '../chaincode'
    ))
    os.environ['GOPATH'] = os.path.abspath(gopath)

    host_ip = socket.gethostbyname(socket.gethostname())
    print(host_ip)
    name = host_ip.encode("utf-8")
    arg2 = base64.b64encode(hashlib.sha256(name).digest())
    args = ["server", arg2]

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
        requestor=user2,
        channel_name='modbuschannel',
        peers=['peer0.org2.example.com'],
        args=args,
        cc_name='registration_cc_v2',
        transient_map=None,  # optional, for private data
        # for being sure chaincode invocation has been commited in the ledger, default is on tx event
        wait_for_event=True,
        # cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
    ))
