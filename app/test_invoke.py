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

###     import json
###     import ecdsa
###     import codecs
###     import base64
###     import struct
###     import hashlib
###     from asn1crypto.core import Sequence
###     
###     secret = '-----BEGIN EC PRIVATE KEY-----MHQCAQEEIB0/t/AxKgqIb+XhPAPKXcZ+CN6/EfEotMv1ROMfXpGPoAcGBSuBBAAKoUQDQgAE+qJKnbVCrP8BZYyzC2O+sboCjZZDFB8whUfjGCaGIN8WfPEbC6jvO50Ic1YQqs81mFpsm3CMFlittb1CHc3hgA==-----END EC PRIVATE KEY-----'
###     publick = '-----BEGIN PUBLIC KEY-----MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE+qJKnbVCrP8BZYyzC2O+sboCjZZDFB8whUfjGCaGIN8WfPEbC6jvO50Ic1YQqs81mFpsm3CMFlittb1CHc3hgA==-----END PUBLIC KEY-----'
###     
###     msg = '{"did": "did:vtn:trustos:company:2","publicKey": "-----BEGIN PUBLIC KEY-----MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE+qJKnbVCrP8BZYyzC2O+sboCjZZDFB8whUfjGCaGIN8WfPEbC6jvO50Ic1YQqs81mFpsm3CMFlittb1CHc3hgA==-----END PUBLIC KEY-----", "hash": "bd945a92d5f849d07b52e1f7cdf895e2552ef542519fbed2196de88f9cef8cab", "signature": "3045022100b8cf1f382a70bf7524051817db9aa017bea056fa0cabb7b6dbf7152ce223edd702200897e7158e4e9b1ccf43fa99a3211221b4800e44fc504cb124f1ecf1408e7d67"}'

##msgCoded = json.dumps(msg)

###     h = hashlib.sha256()
###     h.update(msg.encode("utf-8"))
###     print(h.hexdigest())
###     print(h.digest())
###     msg_sha256_hash = h.digest()

###     sk = ecdsa.SigningKey.from_pem(open("privk.pem").read())
###     sig = sk.sign_digest(
###         msg_sha256_hash,
###         sigencode=ecdsa.util.sigencode_der,
###     )

###     print(sig)

###     sigCoded = codecs.encode(sig, 'hex_codec')
###     print(sigCoded)

##########  Inspect the Signature
###     seq = Sequence.load(sig)
###     print(seq.native)
###     for k, v in seq.native.items():
###         print("%s => %X" % (k, v))

#####   Base64-Encode the Signature for Transmission
###     b64hash = base64.b64encode(msg.encode("utf-8"))
###     print(b64hash)

###     b64sig = base64.b64encode(sig)
###     print(str(b64sig))

###     payload = h.hexdigest() + '.' + sigCoded.decode('utf-8')
###     payload = str(b64hash) + '.' + str(b64sig)
###     print(payload.encode('utf-8'))



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

args = ["{\"did\":\"did:vtn:trustos:company:2\",\"payload\":\"eyJkaWQiOiAiZGlkOnZ0bjp0cnVzdG9zOmNvbXBhbnk6MiIsInB1YmxpY0tleSI6ICItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLU1GWXdFQVlIS29aSXpqMENBUVlGSzRFRUFBb0RRZ0FFK3FKS25iVkNyUDhCWll5ekMyTytzYm9DalpaREZCOHdoVWZqR0NhR0lOOFdmUEViQzZqdk81MEljMVlRcXM4MW1GcHNtM0NNRmxpdHRiMUNIYzNoZ0E9PS0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLSIsICJoYXNoIjogImJkOTQ1YTkyZDVmODQ5ZDA3YjUyZTFmN2NkZjg5NWUyNTUyZWY1NDI1MTlmYmVkMjE5NmRlODhmOWNlZjhjYWIiLCAic2lnbmF0dXJlIjogIjMwNDUwMjIxMDBiOGNmMWYzODJhNzBiZjc1MjQwNTE4MTdkYjlhYTAxN2JlYTA1NmZhMGNhYmI3YjZkYmY3MTUyY2UyMjNlZGQ3MDIyMDA4OTdlNzE1OGU0ZTliMWNjZjQzZmE5OWEzMjExMjIxYjQ4MDBlNDRmYzUwNGNiMTI0ZjFlY2YxNDA4ZTdkNjcifQ==\"}"]
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