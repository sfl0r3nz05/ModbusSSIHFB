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

# 1. Generar el did para el issuer
#path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
pathwallet = './walletKey.json'
pathwalletDid = './walletDid.json'
path_priv_key = './privk.key'
createDID(pathwallet, pathwalletDid, path_priv_key)


# 2. Generar payload para registrar la identidad del issuer
#path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
path_priv_key = './privk.key'
did_wallet_path = './walletDid.json'
payload = payloadToRegisterDid(path_priv_key, did_wallet_path)

print(payload)

# 3. Registrar la identity del issuer
net_profile = '../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDid(net_profile, organization, user, channel,
                   peer, chaincode, function, payload)


# 4. Generar payload para Registrar al issuer como issuer   
#path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
path_priv_key = './privk.key'
did_wallet_path = './walletDid.json'
method = "setIssuer"
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
payload = payloadToRegisterEntity(path_priv_key, did_wallet_path, method, issuer)

print(payload)

# 5. Registrar el issuer como issuer
net_profile = '../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerEntity(net_profile, organization, user, channel,
                   peer, chaincode, function, payload)