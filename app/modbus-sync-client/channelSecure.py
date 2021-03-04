#!/usr/bin/env python
import os
from pymodbus.client.sync import ModbusTlsClient
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1
os.environ['IP_SERVER']
def run_sync_client():
    client_cert = 'client.crt'
    client_key = 'privk.key'
    did_wallet_path = "walletDid.json"
    client = ModbusTlsClient(host=os.getenv('IP_SERVER'), port=8020, sslctx=None, certfile=client_cert, keyfile=client_key, did_wallet_path=did_wallet_path)
    socket, B = client.connect()
    print("B")
    print(B)
    client.close()

if __name__ == "__main__":
    run_sync_client()