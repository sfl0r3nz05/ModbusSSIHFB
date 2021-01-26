import os
import asyncio
from hfc.fabric import Client
import json


def querySyncServer():
    loop = asyncio.get_event_loop()

    cli = Client(
        net_profile="../connection-profile/2org_2peer_solo/network.json")
    user2 = cli.get_user('org2.example.com', 'User1')
    cli.new_channel('modbuschannel')
    gopath_bak = os.environ.get('GOPATH', '')
    gopath = os.path.normpath(os.path.join(
        os.path.dirname(os.path.realpath('__file__')),
        '../chaincode'
    ))
    os.environ['GOPATH'] = os.path.abspath(gopath)

    # Query a chaincode
    args = ["client"]
    # The response should be true if succeed#
    response = loop.run_until_complete(cli.chaincode_query(
        requestor=user2,
        channel_name='modbuschannel',
        peers=['peer0.org2.example.com'],
        args=args,
        cc_name='registration_cc_v2'
    ))
    response = json.loads(response)
    return(response)
