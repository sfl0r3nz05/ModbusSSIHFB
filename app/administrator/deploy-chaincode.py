import os
import asyncio
from hfc.fabric import Client

did = ""
controller = ""
publicKey = ""

loop = asyncio.get_event_loop()

cli = Client(net_profile="../connection-profile/2org_2peer_solo/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')
org2_admin = cli.get_user('org2.example.com', 'Admin')

# Make the client know there is a channel in the network
cli.new_channel('modbuschannel')

# Install Example Chaincode to Peers
# GOPATH setting is only needed to use the example chaincode inside sdk
gopath_bak = os.environ.get('GOPATH', '')
gopath = os.path.normpath(os.path.join(
    os.path.dirname(os.path.realpath('__file__')),
    '../chaincode'
))
os.environ['GOPATH'] = os.path.abspath(gopath)

print("gopath", gopath)

# The response should be true if succeed
responses = loop.run_until_complete(cli.chaincode_install(
    requestor=org1_admin,
    peers=['peer0.org1.example.com'],
    cc_path='github.com/ssi_cc',
    cc_name='ssi_cc',
    cc_version='v1.0'
))

# The response should be true if succeed
responses = loop.run_until_complete(cli.chaincode_install(
    requestor=org2_admin,
    peers=['peer0.org2.example.com'],
    cc_path='github.com/ssi_cc',
    cc_name='ssi_cc',
    cc_version='v1.0'
))

# Instantiate Chaincode in Channel, the response should be true if succeed
args = ["{\"did\":\"did:vtn:trustid:29222201b6662e5b2a07815f7f98b8653b306e3af3830dbaf2387da49ec744db\",\"controller\":\"did:vtn:trustid:29222201b6662e5b2a07815f7f98b8653b306e3af3830dbaf2387da49ec744db\",\"publicKey\":\"-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzP4bEUzWUJQh+gm9apHT6H1myWMqje4I3+F0d4NSPV8Y3HG0mOYr034fx34je9F82+YpToOO5utbQFlDTmCcI3S2hO4oNwV4xuvt+DCMm2QsYOPCy8BjMHFHiOxTVzlDNaq9YVrGeiEY6+e5e5c61y+Yi5YeaRld0RLBWkIfaQIAQyx/FgYFpzDDhxB/TznO9hiw5O5/MFqVOKFEhjT3ndXPRuHUi1F5BfidzlKzfU8G9LO4M+VLzRwnsWGsrgdyQwK8SG9RhcYwPBKMqxwdyUwwccX3DEovshPMxEdPGaj1zuJuAuJlcd504FZDSqszcTjbdSGUgivVWMv8HvRIoQIDAQAB-----END PUBLIC KEY-----\"}"]

# policy, see https://hyperledger-fabric.readthedocs.io/en/release-1.4/endorsement-policies.html
policy = {
    'identities': [
        {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
    ],
    'policy': {
        '1-of': [
            {'signed-by': 0},
        ]
    }
}
response = loop.run_until_complete(cli.chaincode_instantiate(
    requestor=org1_admin,
    channel_name='modbuschannel',
    peers=['peer0.org1.example.com'],
    args=args,
    cc_name='ssi_cc',
    cc_version='v1.0',
    # cc_endorsement_policy=policy,  # optional, but recommended
    collections_config=None,  # optional, for private data policy
    transient_map=None,  # optional, for private data
    wait_for_event=True  # optional, for being sure chaincode is instantiated#
))

print("response", response)

# Query a chaincode, [a]
args = ["did:vtn:trustid:29222201b6662e5b2a07815f7f98b8653b306e3af3830dbaf2387da49ec744db"]
# The response should be true if succeed
response = loop.run_until_complete(cli.chaincode_query(
    requestor=org1_admin,
    channel_name='modbuschannel',
    peers=['peer0.org2.example.com'],
    args=args,
    cc_name='ssi_cc',
    fcn='query',
))
