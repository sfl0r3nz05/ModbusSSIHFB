import sys
from hfbssisdk.src.hfbssi.did import createDID
from hfbssisdk.src.hfbssi.registerDid import registerDid
from hfbssisdk.src.hfbssi.registerDid import queryDid
from hfbssisdk.src.hfbssi.registerDid import payloadToRegisterDid
#   from hfbssisdk.src.hfbssi.entity import registerEntity
#   from hfbssisdk.src.hfbssi.did import generateDIDentity
#   from hfbssisdk.src.hfbssi.registerDid import queryDidDoc
#   from hfbssisdk.src.hfbssi.registerDid import registerDidDoc
#   from hfbssisdk.src.hfbssi.entity import payloadToRegisterEntity
#   from hfbssisdk.src.hfbssi.verifySignature import verifySignature


############################################################ ADMIN ###############################################################################
# 1. Generar el did para el issuer
pathwallet = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletKey.json'
pathwalletDid = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletDid.json'
path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
createDID(pathwallet, pathwalletDid, path_priv_key)

# 2. Generar payload para registrar el issuer
path_priv_key = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
did_wallet_path = '/home/ubuntu/ModbusSSIHFB/app/administrator/walletDid.json'
payload = payloadToRegisterDid(path_priv_key, did_wallet_path)
print(payload)

# 3. Register identity para el issuer
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'ssi_cc'
function = 'proxy'
registerDid(net_profile, organization, user, channel,
                   peer, chaincode, function, payload)

############################################################ ADMIN ###############################################################################


#    # 4. Generar payload para registrar el cliente
#    pathprivKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
#    did_client, public_key_client = payloadToRegisterEntity(pathprivKey)
#    print(did_client)
#    print(public_key_client)
#    
#    # 5. Register client (No irá en este archivo, lo hace el client)
#    net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#    organization = 'org1.example.com'
#    user = 'Admin'
#    channel = 'modbuschannel'
#    peer = 'peer0.org1.example.com'
#    chaincode = 'proxy_cc'
#    function = 'entityRegister'
#    registerEntity(net_profile, organization, user, channel,
#                   peer, chaincode, function, did_client, 'did:vtn:trustid:d7104427989de1fa5729c68f8cb767bb0740ecd65b3b080e9a725a04297f9641', public_key_client)
#    
#    # 6. Generar payload para registrar el server
#    pathprivKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
#    did_server, public_key_server = payloadToRegisterEntity(pathprivKey)
#    print(did_server)
#    print(public_key_server)
#    
#    # 7. Register server (No irá en este archivo, lo hace el server)
#    net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#    organization = 'org1.example.com'
#    user = 'Admin'
#    channel = 'modbuschannel'
#    peer = 'peer0.org2.example.com'
#    chaincode = 'proxy_cc'
#    function = 'entityRegister'
#    registerEntity(net_profile, organization, user, channel,
#                   peer, chaincode, function, did_server, 'did:vtn:trustid:d7104427989de1fa5729c68f8cb767bb0740ecd65b3b080e9a725a04297f9641', public_key_server)
#    
#    # 8. El administrador crea el didDoc for client belonging Org1 (Depende de que 4 se haya llevado a cabo)
#    pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-client/wallet.json'
#    pathprivKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
#    pathpubKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/admincerts/User1@org1.example.com-cert.pem'
#    did, controller, pubKey, payload = generateDIDentity(
#        pathwallet, pathpubKey, pathprivKey, 0, 5020, 6, 1000, 0)
#    
#    # 9. El administrador registra el didDoc for client belonging Org1 (Depende de que 4 se haya llevado a cabo)
#    net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#    organization = 'org1.example.com'
#    user = 'Admin'
#    channel = 'modbuschannel'
#    peer = 'peer0.org1.example.com'
#    chaincode = 'proxy_cc'
#    function = 'didDocRegister'
#    registerDidDoc(net_profile, organization, user, channel,
#                   peer, chaincode, function, did, controller, pubKey, payload)
#    
#    # 10. El administrador crea el didDoc for server belonging Org1 (Depende de que 5 se haya llevado a cabo)
#    pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/wallet.json'
#    pathprivKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
#    pathpubKey = '/home/ubuntu/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/signcerts/User1@org2.example.com-cert.pem'
#    did, controller, pubKey, payload = generateDIDentity(
#        pathwallet, pathpubKey, pathprivKey, 1, 0, 0, 0, 0)
#    
#    # 11. El administrador registra el didDoc for server belonging Org1 (Depende de que 5 se haya llevado a cabo)
#    net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#    organization = 'org1.example.com'
#    user = 'Admin'
#    channel = 'modbuschannel'
#    peer = 'peer0.org1.example.com'
#    chaincode = 'proxy_cc'
#    function = 'didDocRegister'
#    registerDidDoc(net_profile, organization, user, channel,
#                   peer, chaincode, function, did, controller, pubKey, payload)
#    
########################################################################################################################################################################################################################################
#net_profile = '../../connection-profile/2org_2peer_solo/network.json'
#organization = 'org1.example.com'
#user = 'Admin'
#channel = 'modbuschannel'
#peer = 'peer0.org1.example.com'
#chaincode = 'proxy_cc'
#function = 'controllerGet'
# pubKey = queryController(net_profile, organization, user, channel,
#                         peer, chaincode, function, did)
#
#
#pathwallet = '/home/ubuntu/ModbusSSIHFB/app/modbus-sync-server/wallet.json'
#reponse = verifySignature(pubKey, pathwallet)
