import sys
from hfbssisdk.src.hfbssi.payload import payloadgen
from hfbssisdk.src.hfbssi.did import generateDIDadmin
from hfbssisdk.src.hfbssi.did import generateDIDentity

# did created for administrator
pathwallet = '/home/santiago/ModbusSSIHFB/app/administrator/wallet.json'
pathwalletDid = '/home/santiago/ModbusSSIHFB/app/administrator/walletDid.json'
path_priv_key = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
generateDIDadmin(pathwallet, pathwalletDid, path_priv_key)

# did created for client belonging Org1
pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-client/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/admincerts/User1@org1.example.com-cert.pem'
generateDIDentity(pathwallet, pathpubKey, pathprivKey)

# did created for server belonging Org2s
pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-server/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/signcerts/User1@org2.example.com-cert.pem'
generateDIDentity(pathwallet, pathpubKey, pathprivKey)

path_priv_key = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
did_wallet_path = ''
did, signature = payloadgen(path_priv_key, did_wallet_path)
print(did)
print(signature)
# createController(net_profile, organization, user, channel, peer, chaincode, function, did, signature)
