import OpenSSL
from hfbssisdk.src.hfbssi.didFromPK import didFromPK
from hfbssisdk.src.hfbssi.getEntity import requestGetEntity
from hfbssisdk.src.hfbssi.getEntity import payloadToGetEntity


def channelVerificationServer(certfile, keyfile, did_wallet_path):
    ### PUBLICKEY FROM CERT  ##########################################################################################
    cafile_byte = open(certfile, 'rt').read()
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cafile_byte)
    pubKeyObject = x509.get_pubkey()
    pubKeyString = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, pubKeyObject)

    ### DID FROM PUBLICKEY ##########################################################################################
    did = didFromPK(pubKeyString)
    payload = payloadToGetEntity(keyfile, did_wallet_path, "getEntity", did)

    net_profile = '../connection-profile/2org_2peer_solo/network.json'
    organization = 'org2.example.com'
    user = 'User1'
    channel = 'modbuschannel'
    peer = 'peer0.org2.example.com'
    chaincode = 'ssi_cc'
    function = 'proxy'
    response = requestGetEntity(net_profile, organization, user, channel, peer, chaincode, function, payload)

    return response