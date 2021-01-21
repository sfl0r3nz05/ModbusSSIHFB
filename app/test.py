from hfc.fabric_ca.caservice import ca_service
from hfc.fabric_network import wallet

casvc = ca_service(target="http://127.0.0.1:7054")
adminEnrollment = casvc.enroll("admin", "adminpw")
secret = adminEnrollment.register("user1")  # register a user to ca
user1Enrollment = casvc.enroll("user1", secret)
new_wallet = wallet.FileSystenWallet()
user_identity = wallet.Identity("user1", user1Enrollment)
user_identity.CreateIdentity(new_wallet)
user1 = new_wallet.create_user("user1", "Org1", "Org1MSP")


casvc = ca_service(target="http://127.0.0.1:8054")
adminEnrollment = casvc.enroll("admin", "adminpw")
secret = adminEnrollment.register("user2")  # register a user to ca
user2Enrollment = casvc.enroll("user2", secret)
new_wallet = wallet.FileSystenWallet()
user_identity = wallet.Identity("user2", user2Enrollment)
user_identity.CreateIdentity(new_wallet)
user1 = new_wallet.create_user("user2", "Org2", "Org2MSP")
