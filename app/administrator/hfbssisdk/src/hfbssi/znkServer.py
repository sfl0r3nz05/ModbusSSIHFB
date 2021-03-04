import json
from hfbssisdk.src.hfbssi.diffie import DiffieHellman
from hfbssisdk.src.hfbssi.didFromPK import didFromWallet
from hfbssisdk.src.hfbssi.getDidDoc import requestDidDoc
from hfbssisdk.src.hfbssi.getDidDoc import payloadToDidDoc

def znkdhServer(did_wallet_path, keyfile):
    ### RECOVER DID DOCUMENT ########################################################################################
    did = didFromWallet(did_wallet_path)

    payload = payloadToDidDoc(keyfile, did_wallet_path, "getDidDoc", did)
    print(payload)

    net_profile = '../connection-profile/2org_2peer_solo/network.json'
    organization = 'org2.example.com'
    user = 'User1'
    channel = 'modbuschannel'
    peer = 'peer0.org2.example.com'
    chaincode = 'ssi_cc'
    function = 'proxy'
    response = requestDidDoc(net_profile, organization, user, channel, peer, chaincode, function, payload)

### RECOVER GENERATOR Y PLAIN NUMBER #############################################################################
    didDocParsed = json.loads(response)

### DEFINE SECRET ################################################################################################
    x=3

### DEFINE BODY A ################################################################################################
    a = DiffieHellman(didDocParsed["serviceGenerator"], didDocParsed["servicePlainNumber"], x)
    print(a.public)
    print(a.secret)