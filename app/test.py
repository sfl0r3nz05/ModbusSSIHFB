#from hfbssi.src.hfbssi.did import generateDID
#from hfc.fabric_ca.caservice import ca_service
#from hfc.fabric_network import wallet

#casvc = ca_service(target="http://127.0.0.1:7054")
#adminEnrollment = casvc.enroll("admin", "adminpw")
# secret = adminEnrollment.register("user1")  # register a user to ca
#user1Enrollment = casvc.enroll("user1", secret)
#new_wallet = wallet.FileSystenWallet()
#user_identity = wallet.Identity("user1", user1Enrollment)
# user_identity.CreateIdentity(new_wallet)
#user1 = new_wallet.create_user("user1", "Org1", "Org1MSP")

#casvc = ca_service(target="http://127.0.0.1:8054")
#adminEnrollment = casvc.enroll("admin", "adminpw")
# secret = adminEnrollment.register("user2")  # register a user to ca
#user2Enrollment = casvc.enroll("user2", secret)
#new_wallet = wallet.FileSystenWallet()
#user_identity = wallet.Identity("user2", user2Enrollment)
# user_identity.CreateIdentity(new_wallet)
#user1 = new_wallet.create_user("user2", "Org2", "Org2MSP")


y = {
    "did": "123",
    "controller": "123",
    "pubKey": "123",
    "privKey": "123"
}

controller = "test"
pathwallet = './hfbssi/src/hfbssi/wallet.json'
pathprivKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_raft/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/e2eede666b16e7f6b8e5f0f8db622d419f637acaf69dbebc5d192e6acc3eeebd_sk'
pathpubKey = '/home/santiago/ModbusSSIHFB/crypto-material/config_raft/crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem'

generateDID(pathwallet, controller, pathpubKey, pathprivKey)
