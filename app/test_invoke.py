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
#pathprivKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_raft/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/e2eede666b16e7f6b8e5f0f8db622d419f637acaf69dbebc5d192e6acc3eeebd_sk'
#pathpubKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_raft/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem'
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


args = ["{\"did\":\"did:vtn:trustos:company:2\",\"payload\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkaWQiOiJkaWQ6dnRuOnRydXN0b3M6Y29tcGFueToyIiwicHVibGljS2V5IjoiLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tTUlJQ0N6Q0NBYkdnQXdJQkFnSVJBTGhjVTFERlgvSytuVmlDbEk2NDJBVXdDZ1lJS29aSXpqMEVBd0l3YVRFTE1Ba0dBMVVFQmhNQ1ZWTXhFekFSQmdOVkJBZ1RDa05oYkdsbWIzSnVhV0V4RmpBVUJnTlZCQWNURFZOaGJpQkdjbUZ1WTJselkyOHhGREFTQmdOVkJBb1RDMlY0WVcxd2JHVXVZMjl0TVJjd0ZRWURWUVFERXc1allTNWxlR0Z0Y0d4bExtTnZiVEFlRncweE9ERXdNVGt3TXpRNE1EQmFGdzB5T0RFd01UWXdNelE0TURCYU1GWXhDekFKQmdOVkJBWVRBbFZUTVJNd0VRWURWUVFJRXdwRFlXeHBabTl5Ym1saE1SWXdGQVlEVlFRSEV3MVRZVzRnUm5KaGJtTnBjMk52TVJvd0dBWURWUVFEREJGQlpHMXBia0JsZUdGdGNHeGxMbU52YlRCWk1CTUdCeXFHU000OUFnRUdDQ3FHU000OUF3RUhBMElBQktYQzJSTUwyS3ZLVytKanR5ZHVoclZyaFh3WGhrb3ZYR3hqNDdkN2RyZ3pCVmFJWjZXU0xoK0JoT2Z1dTNFa0ZqYlp3bXZOQTRxMTZ5QjR6NkpJTmZ5alRUQkxNQTRHQTFVZER3RUIvd1FFQXdJSGdEQU1CZ05WSFJNQkFmOEVBakFBTUNzR0ExVWRJd1FrTUNLQUlLcU1qb3Bna3ViRDUycGRKQXNkWEtBS0VqWjVyMlhIOTgrUTJhQTg3ckhKTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFDbEdnbjhrbW05N0U4WkpUQWdhSTBBMmdoNGgxM042LzN5c3AzMWV6Yjd2QUlnVmp3Ym5zdVFSRHErdWRvR3JOTW0xNjNvUXFVNlZJWW5VWlpHenVVV2g1dz0tLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tIn0.6n4OLloJJVxDTUa43ls5w8-LhRJstLtBRkxDmp3e_Us\"}"]
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

### secret = 'MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgj/ycfnwThLUm9tYkiHqTb3bT/loj1zWQEa1QEKNeeuWhRANCAASlwtkTC9irylviY7cnboa1a4V8F4ZKL1xsY+O3e3a4MwVWiGelki4fgYTn7rtxJBY22cJrzQOKtesgeM+iSDX8'
### publick = '-----BEGIN CERTIFICATE-----MIICCzCCAbGgAwIBAgIRALhcU1DFX/K+nViClI642AUwCgYIKoZIzj0EAwIwaTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBGcmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRcwFQYDVQQDEw5jYS5leGFtcGxlLmNvbTAeFw0xODEwMTkwMzQ4MDBaFw0yODEwMTYwMzQ4MDBaMFYxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJhbmNpc2NvMRowGAYDVQQDDBFBZG1pbkBleGFtcGxlLmNvbTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABKXC2RML2KvKW+JjtyduhrVrhXwXhkovXGxj47d7drgzBVaIZ6WSLh+BhOfuu3EkFjbZwmvNA4q16yB4z6JINfyjTTBLMA4GA1UdDwEB/wQEAwIHgDAMBgNVHRMBAf8EAjAAMCsGA1UdIwQkMCKAIKqMjopgkubD52pdJAsdXKAKEjZ5r2XH98+Q2aA87rHJMAoGCCqGSM49BAMCA0gAMEUCIQClGgn8kmm97E8ZJTAgaI0A2gh4h13N6/3ysp31ezb7vAIgVjwbnsuQRDq+udoGrNMm163oQqU6VIYnUZZGzuUWh5w=-----END CERTIFICATE-----'
### 
### 
### claims = {
###             "did": "did:vtn:trustos:company:2",
###             "publicKey": str(publick)
###         }
### 
### from jose import jws
### signed = jws.sign(claims, secret, algorithm='HS256')
### print(signed)
### 
### jws.verify(signed, secret, algorithms=['HS256'])