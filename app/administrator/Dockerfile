FROM ubuntu:latest
RUN apt-get update -y 
RUN apt-get install -y python3.8
RUN apt install -y python3-pip
RUN apt install -y git 
RUN apt install make
RUN pip3 install asn1crypto
RUN pip3 install jwt
RUN pip3 install ecdsa
RUN pip3 install PyJWT
RUN pip3 install cryptography
RUN git clone https://github.com/hyperledger/fabric-sdk-py.git && cd fabric-sdk-py && make install 
RUN cd ..
ADD configtxgen bin/configtxgen