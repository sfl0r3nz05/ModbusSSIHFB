import sys
from hfbssisdk.src.hfbssi.did import createDID
from hfbssisdk.src.hfbssi.registerDid import registerDid
from hfbssisdk.src.hfbssi.registerDid import payloadToRegisterDid
from hfbssisdk.src.hfbssi.registerEntity import payloadToRegisterIssuer
#   from hfbssisdk.src.hfbssi.entity import registerEntity
#   from hfbssisdk.src.hfbssi.did import generateDIDentity
#   from hfbssisdk.src.hfbssi.registerDid import queryDidDoc
#   from hfbssisdk.src.hfbssi.registerDid import registerDidDoc
#   from hfbssisdk.src.hfbssi.entity import payloadToRegisterEntity
#   from hfbssisdk.src.hfbssi.verifySignature import verifySignature


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
payload = payloadToRegisterIssuer(path_priv_key, did_wallet_path)

# 5. Registrar el issuer como issuer
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDid(net_profile, organization, user, channel,
                   peer, chaincode, function, payload)

############################################################ ADMIN ###################################################################################################################################################################

############################################################ CLIENT ##################################################################################################################################################################

#    # 4. Generar el did para el client
#    pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletKey.json'
#    pathwalletDid = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
#    path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
#    createDID(pathwallet, pathwalletDid, path_priv_key)
#    
#    
#    # 5. Generar payload para registrar el issuer
#    path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
#    did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/walletDid.json'
#    payload = payloadToRegisterDid(path_priv_key, did_wallet_path)
#    
#    
#    # 6. Register identity para el issuer
#    net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#    organization = 'org1.example.com'
#    user = 'User1'
#    channel = 'modbuschannel'
#    peer = 'peer0.org1.example.com'
#    chaincode = 'ssi_cc'
#    function = 'proxy'
#    registerDid(net_profile, organization, user, channel,
#                       peer, chaincode, function, payload)
#    
#    ############################################################ CLIENT ##################################################################################################################################################################
#    
#    ############################################################ SERVER ##################################################################################################################################################################
#    
#    # 7. Generar el did para el client
#    pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletKey.json'
#    pathwalletDid = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
#    path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
#    createDID(pathwallet, pathwalletDid, path_priv_key)
#    
#    
#    # 8. Generar payload para registrar el issuer
#    path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
#    did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/walletDid.json'
#    payload = payloadToRegisterDid(path_priv_key, did_wallet_path)
#    
#    
#    # 9. Register identity para el issuer
#    net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#    organization = 'org2.example.com'
#    user = 'User1'
#    channel = 'modbuschannel'
#    peer = 'peer0.org2.example.com'
#    chaincode = 'ssi_cc'
#    function = 'proxy'
#    registerDid(net_profile, organization, user, channel,
#                       peer, chaincode, function, payload)
#    
#    ############################################################ SERVER ##################################################################################################################################################################