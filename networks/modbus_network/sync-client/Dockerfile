FROM ubuntu:latest
RUN apt-get update -y 
RUN apt-get install -y python3.7
RUN apt install -y python3-pip
RUN apt install -y git
RUN pip3 install -U pymodbus[twisted]
RUN pip3 install jwt
RUN git clone https://github.com/hyperledger/fabric-sdk-py.git && cd fabric-sdk-py && make install