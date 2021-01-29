import os
import asyncio
from hfc.fabric import Client


def payloadToRegisterEntity(path_priv_key, did_wallet_path):
    return 1


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
