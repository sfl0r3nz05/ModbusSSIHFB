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


############################################################ ADMIN ##################################################################################################################################################################
# 1. Generar el did para el issuer
#path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
pathwallet = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletKey.json'
pathwalletDid = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletDid.json'
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/administrator/privk.key'
createDID(pathwallet, pathwalletDid, path_priv_key)

# 2. Generar payload para registrar la identidad del issuer
#path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/administrator/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletDid.json'
payload = payloadToRegisterDid(path_priv_key, did_wallet_path)


# 3. Registrar la identity del issuer
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
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
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/administrator/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletDid.json'
method = "setIssuer"
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
payload = payloadToRegisterEntity(path_priv_key, did_wallet_path, method, issuer)


# 5. Registrar el issuer como issuer
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerEntity(net_profile, organization, user, channel,
                   peer, chaincode, function, payload)

############################################################ ADMIN ###################################################################################################################################################################


############################################################ CLIENT ##################################################################################################################################################################
# 6. Generar el did para el client
pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletKey.json'
pathwalletDid = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
createDID(pathwallet, pathwalletDid, path_priv_key)


# 7. Generar payload para registrar el cliente
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
payload = payloadToRegisterDid(path_priv_key, did_wallet_path)


# 8. Register identity para el issuer
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDid(net_profile, organization, user, channel, 
                    peer, chaincode, function, payload)


# 9. Generar payload para Registrar al cliente como entidad
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
method = "setEntity"
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
payload = payloadToRegisterEntity(path_priv_key, did_wallet_path, method, issuer)


# 10. Registrar el cliente como entidad
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerEntity(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)


# 11. El cliente crea el DidDoc
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDidDoc.json'
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
createDidDocClient(path_priv_key, did_wallet_path, wallet_DidDoc, issuer)
#    ############################################################ CLIENT ##################################################################################################################################################################


#    ############################################################ ADMIN ##################################################################################################################################################################
# 12. El admin firma el DidDoc una vez creado por el cliente
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDidDoc.json'
adminSignature(path_priv_key, wallet_DidDoc)
#    ############################################################ ADMIN ##################################################################################################################################################################


#    ############################################################ CLIENT ##################################################################################################################################################################
# 13. El cliente countersignature el DidDoc una vez creado por el cliente
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDidDoc.json'
counterSignature(path_priv_key, wallet_DidDoc)

# 14. El cliente prepara el payload para registrar
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDidDoc.json'
method = "setDidDoc"
payload = payloadToRegisterDidDoc(path_priv_key, did_wallet_path, wallet_DidDoc, method)


# 15. El cliente Registra el DidDoc
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDidDoc(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)
#    ############################################################ CLIENT ##################################################################################################################################################################


#    ############################################################ SERVER ##################################################################################################################################################################
# 16. Generar el did para el client
pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletKey.json'
pathwalletDid = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
createDID(pathwallet, pathwalletDid, path_priv_key)


# 17. Generar payload para registrar el issuer
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
payload = payloadToRegisterDid(path_priv_key, did_wallet_path)


# 18. Register identity para el issuer
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org2.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org2.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDid(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)


# 19. Generar payload para Registrar al cliente como entidad
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
method ="setEntity"
issuer ="did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
payload = payloadToRegisterEntity(path_priv_key, did_wallet_path, method, issuer)


# 20. Registrar el cliente como entidad
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org2.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org2.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerEntity(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)


# 21. El server crea el DidDoc como entidad
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDidDoc.json'
issuer = "did:vtn:trustid:e320a9308621efa599ca7b9c2462ac05421dfe6ae4cd7dd91132ace1a4f6829b"
port = "802"
fnc = "5"
address = "10"
offset = "10"
createDidDocServer(path_priv_key, did_wallet_path, wallet_DidDoc, issuer, port, fnc, address, offset)
############################################################# SERVER ##################################################################################################################################################################


############################################################# ADMIN ##################################################################################################################################################################
# 22. El admin firma el DidDoc una vez creado por el server
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDidDoc.json'
adminSignature(path_priv_key, wallet_DidDoc)
############################################################# ADMIN ##################################################################################################################################################################


############################################################# SERVER ##################################################################################################################################################################
# 23. El servidor countersignature el DidDoc una vez creado por el server
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDidDoc.json'
counterSignature(path_priv_key, wallet_DidDoc)

# 24. El server prepara el payload para registrar el DidDoc
path_priv_key = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/privk.key'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
wallet_DidDoc = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDidDoc.json'
method = "setDidDoc"
payload = payloadToRegisterDidDoc(path_priv_key, did_wallet_path, wallet_DidDoc, method)


# 25. El servidor Registra el DidDoc
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org2.example.com'
user = 'User1'
channel = 'modbuschannel'
peer = 'peer0.org2.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDidDoc(net_profile, organization, user, channel,
                    peer, chaincode, function, payload)
############################################################# SERVER ##################################################################################################################################################################