# HFB-network

# INSTALL PIP MODULE

1. pip install hfc-py
2. pip3 install asyncio
3. pip3 install fabric-sdk-py


## SET ENVIRONMENTAL VARIABLES

1. export FABRIC_VERSION=1.4.6
2. export FABRIC_CA_VERSION=1.4.6

## CASE SOLO WITH GOLEVELDB

1. Crypto package

   e.g. sudo cp -rf /home/ubuntu/go/src/golang.org /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src

2. gopkg.in package

   e.g. sudo cp -rf /home/ubuntu/go/src/gopkg.in /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src

3. log package
e.g.
   sudo mkdir /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src/github.com/log

   e.g. sudo cp -rf /home/ubuntu/ModbusSSIHFB/chaincode/src/github.com/ssi_cc/logger.go /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src/github.com/log

4. logrus package
e.g.    
   git clone https://github.com/sirupsen/logrus.git
   
   sudo mkdir /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src/github.com/sirupsen/
   
   sudo mv -f /home/ubuntu/logrus /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src/github.com/sirupsen

5. golang.org
e.g.
   go get -u golang.org/x/sys
   sudo cp -rf /home/ubuntu/go/src/golang.org/x/sys /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src/golang.org/x/

   go get github.com/google/uuid
   sudo cp -rf /home/ubuntu/go/src/github.com/google /var/lib/docker/overlay2/5eb7186e78e0e9e4a6ee957f414144e5d40349e04aaf7fb75f59c65b4a9e0628/diff/opt/gopath/src/github.com/

6. How test
   cd app/administrator
   python3 did-creator.py

7. openssl ecparam -name prime256v1 -genkey -noout -out server.key
8. openssl req -new -key server.key -x509 -nodes -days 365 -out server.pem
9. sudo update-ca-certificates

9. docker build -t modbus-sync-base .
10. docker tag ab71c44c0fe9 sflorenz05/modbusssihfb:modbus-sync-base
11. docker push sflorenz05/modbusssihfb:modbus-sync-base