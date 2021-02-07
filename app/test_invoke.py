#from hfbssi.src.hfbssi.did import generateDID
#from hfc.fabric_ca.caservice import ca_service
#from hfc.fabric_network import wallet

#casvc = ca_service(target="http://127.0.0.1:7054")
#adminEnrollment = casvc.enroll("admin", "adminpw")
# secret = adminEnrollment.register("user1")  # register a user to ca
#user1Enrollment = casvc.enroll("user1", secret)
#new_wallet = wallet.FileSystenWallet()
#user_identity = wallet.Identity("user1", user1Enrollment)
# user_identity.CreateIdentity(new_wallet)
#user1 = new_wallet.create_user("user1", "Org1", "Org1MSP")

#casvc = ca_service(target="http://127.0.0.1:8054")
#adminEnrollment = casvc.enroll("admin", "adminpw")
# secret = adminEnrollment.register("user2")  # register a user to ca
#user2Enrollment = casvc.enroll("user2", secret)
#new_wallet = wallet.FileSystenWallet()
#user_identity = wallet.Identity("user2", user2Enrollment)
# user_identity.CreateIdentity(new_wallet)
#user1 = new_wallet.create_user("user2", "Org2", "Org2MSP")


# y = {
#    "did": "123",
#    "controller": "123",
#    "pubKey": "123",
#    "privKey": "123"
# }
#
#controller = "test"
#pathwallet = './hfbssi/src/hfbssi/wallet.json'
#pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_raft/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/e2eede666b16e7f6b8e5f0f8db622d419f637acaf69dbebc5d192e6acc3eeebd_sk'
#pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_raft/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem'
#
#generateDID(pathwallet, controller, pathpubKey, pathprivKey)

##############################################################################################################################################
import os
import asyncio
import base64
import hashlib
import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()
cli = Client(
    net_profile="../connection-profile/2org_2peer_solo/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')
org2_admin = cli.get_user('org2.example.com', 'Admin')
cli.new_channel('modbuschannel')
gopath_bak = os.environ.get('GOPATH', '')
gopath = os.path.normpath(os.path.join(
    os.path.dirname(os.path.realpath('__file__')),
    '../chaincode'
))
os.environ['GOPATH'] = os.path.abspath(gopath)
#args = ["did:vtn:trustos:trienekens:0", "did:vtn:trustos:trienekens:0", "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7NBDzVMESXU/yuARe7YU\nGrkgNMZh5eA5w3PgxgYZf/isDLPHvmSM2Q9cTauDroriGInikQxtZ/CI4+9Qi4Rd\nJCHjeWhzw0hTIXhHoohyo9QTbUVetb4RBDJEcNqFrpztAojn8Ib5EF2soBFtBLyT\nguxlizcWwTZvv+KxHGBg/tUE7JIqw3YzmEK31faR2HhkPPqxTQ9F+h4SOnY9e6Cf\nh75PpjouzarpntSVkAqv/Ot5kV3O4TcWhB0vUr/HZwx2iX+LEyYock8Sx4Op20/g\n7k3J3rYhMGTHfkKMhZjX9QoZ8uBRiSxieAaia0yZSIcycgE6Aqu6KT+WaQn4bCnh\nwQIDAQAB\n-----END PUBLIC KEY-----"]
# response = loop.run_until_complete(cli.chaincode_invoke(
#    requestor=org1_admin,
#    channel_name='modbuschannel',
#    peers=['peer0.org1.example.com'],
#    args=args,
#    cc_name='proxy_cc',
#    transient_map=None,  # optional, for private data
#    wait_for_event=True,
#    fcn='entityRegister',
# ))

args = ["{\"did\":\"did:vtn:trustos:company:0\",\"payload\":\"eyJhbGdvcml0aG0iOiJQUzI1NiIsImFsZyI6IlBTMjU2In0.eyJmdW5jdGlvbiI6ImNyZWF0ZVNlbGZJZGVudGl0eSIsInBhcmFtcyI6eyJkaWQiOiJkaWQ6dnRuOnRydXN0b3M6dGVsZWZvbmljYToyIiwicHVibGljS2V5IjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBdTA0ZTlWTE5uMUpIZ1lOSU1SclVcblE0SkhoSG4wd1p4UENEOWtjUHo2M1NNQmlZbkN0Uk0yNHBLODZnQWFUdU00RDhWMkxqckE2ZHZCV3dCT2YydUZcbi80aXJJUlhNT2FJNTh1dFhFQ3NBMHI2Q3cyU3BDWVNWOEJLMXk4aHBuc3cwMi9UMHhZUkRiRnFmaHZxYQ\"}"]
response = loop.run_until_complete(cli.chaincode_invoke(
    requestor=org1_admin,
    channel_name='modbuschannel',
    peers=['peer0.org1.example.com'],
    args=args,
    cc_name='ssi_cc',
    transient_map=None,  # optional, for private data
    wait_for_event=True,
    fcn='proxy',
))

print (response)

#name = '192.168.127.41'
#arg2 = base64.b64encode(hashlib.sha256(name.encode('utf-8')).digest())
#args = ["client", arg2]
# The response should be true if succeed
# response = loop.run_until_complete(cli.chaincode_invoke(
#    requestor=org1_admin,
#    channel_name='modbuschannel',
#    peers=['peer0.org1.example.com'],
#    args=args,
#    cc_name='registration_cc_v2',
#    transient_map=None,  # optional, for private data
#    # for being sure chaincode invocation has been commited in the ledger, default is on tx event
#    wait_for_event=True,
#    # cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
# ))
