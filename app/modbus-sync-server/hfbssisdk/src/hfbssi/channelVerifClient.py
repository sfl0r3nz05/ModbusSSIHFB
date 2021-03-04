import OpenSSL
from hfbssisdk.src.hfbssi.didFromPK import didFromPK
from hfbssisdk.src.hfbssi.getEntity import requestGetEntity
from hfbssisdk.src.hfbssi.getEntity import payloadToGetEntity

def channelVerificationClient(cert, keyfile, did_wallet_path):
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
    pubKeyObject = x509.get_pubkey()
    pubKeyString = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, pubKeyObject)

    did = didFromPK(pubKeyString)
    payload = payloadToGetEntity(keyfile, did_wallet_path, "getEntity", did)

    net_profile = '../connection-profile/2org_2peer_solo/network.json'
    organization = 'org1.example.com'
    user = 'User1'
    channel = 'modbuschannel'
    peer = 'peer0.org1.example.com'
    chaincode = 'ssi_cc'
    function = 'proxy'
    response = requestGetEntity(net_profile, organization, user, channel, peer, chaincode, function, payload)

    return response, did