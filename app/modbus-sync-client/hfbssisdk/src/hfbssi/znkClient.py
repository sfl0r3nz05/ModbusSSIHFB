import json
from hfbssisdk.src.hfbssi.diffie import DiffieHellman
from hfbssisdk.src.hfbssi.getDidDoc import requestDidDoc
from hfbssisdk.src.hfbssi.getDidDoc import payloadToDidDoc

def znkdhClient(did_wallet_path, keyfile, did):
    ### RECOVER DID DOCUMENT ########################################################################################
        payload = payloadToDidDoc(keyfile, did_wallet_path, "getDidDoc", did)
        print(payload)

        net_profile = '../connection-profile/2org_2peer_solo/network.json'
        organization = 'org1.example.com'
        user = 'User1'
        channel = 'modbuschannel'
        peer = 'peer0.org1.example.com'
        chaincode = 'ssi_cc'
        function = 'proxy'
        response = requestDidDoc(net_profile, organization, user, channel, peer, chaincode, function, payload)

### RECOVER GENERATOR Y PLAIN NUMBER #############################################################################
        didDocParsed = json.loads(response)
        print(didDocParsed["serviceGenerator"])
        print(didDocParsed["servicePlainNumber"])

### DEFINE SECRET ################################################################################################
        y=4

### DEFINE BODY B ################################################################################################
        b = DiffieHellman(didDocParsed["serviceGenerator"], didDocParsed["servicePlainNumber"], y)
        print(b.public)
        print(b.secret)
        return b.public
