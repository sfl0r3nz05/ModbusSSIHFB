import sys
from hfbssisdk.src.hfbssi.did import generateDIDentity
from hfbssisdk.src.hfbssi.did import generateDIDadmin

# did created for client belonging Org1
controller = "test"
pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-client/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/admincerts/User1@org1.example.com-cert.pem'
generateDIDentity(pathwallet, controller, pathpubKey, pathprivKey)

# did created for server belonging Org2
controller = "test"
pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-server/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/signcerts/User1@org2.example.com-cert.pem'
generateDIDentity(pathwallet, controller, pathpubKey, pathprivKey)

# did created for administrator
controller = "test"
pathwallet = '/home/santiago/ModbusSSIHFB/app/administrator/wallet.json'
generateDIDadmin(pathwallet, controller)
