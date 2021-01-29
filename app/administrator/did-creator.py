import sys
from hfbssisdk.src.hfbssi.did import generateDIDadmin
from hfbssisdk.src.hfbssi.entity import registerEntity
from hfbssisdk.src.hfbssi.did import generateDIDentity
from hfbssisdk.src.hfbssi.controller import queryDidDoc
from hfbssisdk.src.hfbssi.controller import registerDidDoc
from hfbssisdk.src.hfbssi.controller import queryController
from hfbssisdk.src.hfbssi.controller import registerController
from hfbssisdk.src.hfbssi.entity import payloadToRegisterEntity
from hfbssisdk.src.hfbssi.verifySignature import verifySignature
from hfbssisdk.src.hfbssi.controller import payloadToRegisterController


# 1. Generar el did para el administrador
pathwallet = '/home/santiago/ModbusSSIHFB/app/administrator/wallet.json'
pathwalletDid = '/home/santiago/ModbusSSIHFB/app/administrator/walletDid.json'
path_priv_key = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
generateDIDadmin(pathwallet, pathwalletDid, path_priv_key)


# 2. Generar payload para registrar el controlador
path_priv_key = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
did_wallet_path = '/home/santiago/ModbusSSIHFB/app/administrator/walletDid.json'
did, payload = payloadToRegisterController(path_priv_key, did_wallet_path)

# 3. Register controller
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'proxy_cc'
function = 'controllerRegister'
registerController(net_profile, organization, user, channel,
                   peer, chaincode, function, did, payload)

# 4. Register client (No irá en este archivo, lo hace el client)
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/admincerts/User1@org1.example.com-cert.pem'


net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'proxy_cc'
function = 'entityRegister'
registerEntity(net_profile, organization, user, channel,
               peer, chaincode, function, 'did:vtn:trustid:beaf4dafac54331621dd6c685248f9e26ee45703a697f571b4d34562bd7c73fb', 'did:vtn:trustid:d7104427989de1fa5729c68f8cb767bb0740ecd65b3b080e9a725a04297f9641', '-----BEGIN CERTIFICATE-----MIICKjCCAdGgAwIBAgIRAOuqO4gIp7Z0qK+nP2m/w0UwCgYIKoZIzj0EAwIwczELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBGcmFuY2lzY28xGTAXBgNVBAoTEG9yZzEuZXhhbXBsZS5jb20xHDAaBgNVBAMTE2NhLm9yZzEuZXhhbXBsZS5jb20wHhcNMTgxMDE5MDM0ODAwWhcNMjgxMDE2MDM0ODAwWjBsMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEWMBQGA1UEBxMNU2FuIEZyYW5jaXNjbzEPMA0GA1UECxMGY2xpZW50MR8wHQYDVQQDDBZVc2VyMUBvcmcxLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWhkliN8d3zX7cBV7gAlRGjoV7euSY759ViJZrW7vGaNDFmFnIop30KT2HT6N7UugHVK4pl1auuDQnkWlYVIRmKNNMEswDgYDVR0PAQH/BAQDAgeAMAwGA1UdEwEB/wQCMAAwKwYDVR0jBCQwIoAga6xgFWY3j82bg8aLlpkNQa21FTJkDesOhPg87B1Yl9IwCgYIKoZIzj0EAwIDRwAwRAIgXwSy7f7+ExoM1/J4bWJTybcO204klB9ry2keH6VG2ekCIHn+OF/3KxNsYSo904Df0PPBgtkZF3njS14Std3S9Mgd-----END CERTIFICATE-----')

# 5. Register server (No irá en este archivo, lo hace el server)
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org2.example.com'
chaincode = 'proxy_cc'
function = 'entityRegister'
registerEntity(net_profile, organization, user, channel,
               peer, chaincode, function, 'did:vtn:trustid:4981f7c8f152f14d009c1b69d4972c84fdb4985055dc33d4d25c821ab015ad7e', 'did:vtn:trustid:d7104427989de1fa5729c68f8cb767bb0740ecd65b3b080e9a725a04297f9641', '-----BEGIN CERTIFICATE-----MIICKjCCAdCgAwIBAgIQZlZer9OVo/b4Qii45sUfEzAKBggqhkjOPQQDAjBzMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEWMBQGA1UEBxMNU2FuIEZyYW5jaXNjbzEZMBcGA1UEChMQb3JnMi5leGFtcGxlLmNvbTEcMBoGA1UEAxMTY2Eub3JnMi5leGFtcGxlLmNvbTAeFw0xODEwMTkwMzQ4MDBaFw0yODEwMTYwMzQ4MDBaMGwxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJhbmNpc2NvMQ8wDQYDVQQLEwZjbGllbnQxHzAdBgNVBAMMFlVzZXIxQG9yZzIuZXhhbXBsZS5jb20wWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASaJG8xzdJwDGoXCqouUZYHCW56Se3sU9OVj+NSGZxetfmm/+aKDqIMEd+bDPVn0HZsZYC/sYWLfwIkvI9V2/4No00wSzAOBgNVHQ8BAf8EBAMCB4AwDAYDVR0TAQH/BAIwADArBgNVHSMEJDAigCDu2ocNKJDV2HmtXnLRQ5pss5b6OW4OCYwI6HNM+hE5jDAKBggqhkjOPQQDAgNIADBFAiEA2Wsm0MmQmVpUMCr+Dxkemho26LkQl6kJaPUnGfhcBncCICuifm6WrpD/Lk80Z4VODaALfq9Wt1ZOxLx3ZWh9uEKK-----END CERTIFICATE-----')

# 6. El administrador crea el didDoc for client belonging Org1 (Depende de que 4 se haya llevado a cabo)
pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-client/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/admincerts/User1@org1.example.com-cert.pem'
did, controller, pubKey, payload = generateDIDentity(
    pathwallet, pathpubKey, pathprivKey, 0, 5020, 6, 1000, 0)

# 7. El administrador registra el didDoc for client belonging Org1 (Depende de que 4 se haya llevado a cabo)
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'proxy_cc'
function = 'didDocRegister'
registerDidDoc(net_profile, organization, user, channel,
               peer, chaincode, function, did, controller, pubKey, payload)

# 8. El administrador crea el didDoc for server belonging Org1 (Depende de que 5 se haya llevado a cabo)
pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-server/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_solo/crypto-config/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/signcerts/User1@org2.example.com-cert.pem'
did, controller, pubKey, payload = generateDIDentity(
    pathwallet, pathpubKey, pathprivKey, 1, 0, 0, 0, 0)

# 9. El administrador registra el didDoc for server belonging Org1 (Depende de que 5 se haya llevado a cabo)
net_profile = '../../connection-profile/2org_2peer_solo/network.json'
organization = 'org1.example.com'
user = 'Admin'
channel = 'modbuschannel'
peer = 'peer0.org1.example.com'
chaincode = 'proxy_cc'
function = 'didDocRegister'
registerDidDoc(net_profile, organization, user, channel,
               peer, chaincode, function, did, controller, pubKey, payload)

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
#pathwallet = '/home/santiago/ModbusSSIHFB/app/modbus-sync-server/wallet.json'
#reponse = verifySignature(pubKey, pathwallet)
