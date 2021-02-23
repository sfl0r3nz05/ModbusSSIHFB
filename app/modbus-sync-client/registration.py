import sys
from hfbssisdk.src.hfbssi.did import createDID
from hfbssisdk.src.hfbssi.didDoc import counterSignature
from hfbssisdk.src.hfbssi.didDoc import adminSignature
from hfbssisdk.src.hfbssi.registerDid import registerDid
from hfbssisdk.src.hfbssi.didDoc import createDidDocClient
from hfbssisdk.src.hfbssi.didDoc import createDidDocServer
from hfbssisdk.src.hfbssi.registerDidDoc import registerDidDoc
from hfbssisdk.src.hfbssi.registerEntity import registerEntity
from hfbssisdk.src.hfbssi.registerDid import payloadToRegisterDid
from hfbssisdk.src.hfbssi.registerEntity import payloadToRegisterEntity
from hfbssisdk.src.hfbssi.registerDidDoc import payloadToRegisterDidDoc


# 6. Generar el did para el client
pathwallet = './walletKey.json'
pathwalletDid = './walletDid.json'
path_priv_key = './privk.key'
createDID(pathwallet, pathwalletDid, path_priv_key)


# 7. Generar payload para registrar el cliente
path_priv_key = './privk.key'
did_wallet_path = './walletDid.json'
payload = payloadToRegisterDid(path_priv_key, did_wallet_path)


# 8. Register identity para el issuer
net_profile = '../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDid(net_profile, organization, user, channel, 
                    peer, chaincode, function, payload)


# 9. Generar payload para Registrar al cliente como entidad
path_priv_key = './privk.key'
did_wallet_path = './walletDid.json'
method = "setEntity"
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
payload = payloadToRegisterEntity(path_priv_key, did_wallet_path, method, issuer)


# 10. Registrar el cliente como entidad
net_profile = '../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerEntity(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)


# 11. El cliente crea el DidDoc
path_priv_key = './privk.key'
did_wallet_path = './walletDid.json'
wallet_DidDoc = './walletDidDoc.json'
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
createDidDocClient(path_priv_key, did_wallet_path, wallet_DidDoc, issuer)


#    ############################################################ ADMIN ##################################################################################################################################################################
# 12. El admin firma el DidDoc una vez creado por el cliente
path_priv_key = './privk.key'
wallet_DidDoc = './walletDidDoc.json'
adminSignature(path_priv_key, wallet_DidDoc)
#    ############################################################ ADMIN ##################################################################################################################################################################


# 13. El cliente countersignature el DidDoc una vez creado por el cliente
path_priv_key = './privk.key'
wallet_DidDoc = './walletDidDoc.json'
counterSignature(path_priv_key, wallet_DidDoc)

# 14. El cliente prepara el payload para registrar
path_priv_key = './privk.key'
did_wallet_path = './walletDid.json'
wallet_DidDoc = './walletDidDoc.json'
method = "setDidDoc"
payload = payloadToRegisterDidDoc(path_priv_key, did_wallet_path, wallet_DidDoc, method)


# 15. El cliente Registra el DidDoc
net_profile = '../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDidDoc(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)