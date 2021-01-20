from app.HFBapp.querySyncClient import querySyncClient
from app.HFBapp.invokeSyncClient import invokeSyncClient
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.mei_message import *
import os
import socket
from time import sleep
import hashlib
import base64

os.environ['IP_SERVER']
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1


def run_sync_client():
    client = ModbusClient(os.getenv('IP_SERVER'), port=5020)
    client.connect()
    print(client.socket)
    print(client.socket.getsockname())
    rq = ReadDeviceInformationRequest(unit=UNIT)
    rr = client.execute(rq)
    print(rr)
    response = querySyncClient()
    message = os.getenv('IP_SERVER')
    message = message.encode("utf-8")
    message = base64.b64encode(hashlib.sha256(message).digest())
    message = message.decode("utf-8")
    if message != response['hash']:
        print("Error en autenticacion")
        print(response)
        print(message)
        return
    while True:
        log.debug("Reading Coils")
        rr = client.read_coils(0, 1, unit=UNIT)
        log.debug(rr)

        log.debug("Write to a Coil and read back")
        rq = client.write_coil(0, True, unit=UNIT)
        rr = client.read_coils(0, 1, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error
        assert(rr.bits[0] == True)          # test the expected value

        log.debug("Write to multiple coils and read back- test 1")
        rq = client.write_coils(1, [True]*8, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error
        rr = client.read_coils(1, 21, unit=UNIT)
        assert(not rr.isError())     # test that we are not an error
        resp = [True]*21
        resp.extend([False]*3)
        assert(rr.bits == resp)         # test the expected value

        log.debug("Write to multiple coils and read back - test 2")
        rq = client.write_coils(1, [False]*8, unit=UNIT)
        rr = client.read_coils(1, 8, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error
        assert(rr.bits == [False]*8)         # test the expected value

        log.debug("Read discrete inputs")
        rr = client.read_discrete_inputs(0, 8, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error

        log.debug("Write to a holding register and read back")
        rq = client.write_register(1, 10, unit=UNIT)
        rr = client.read_holding_registers(1, 1, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error
        assert(rr.registers[0] == 10)       # test the expected value

        log.debug("Write to multiple holding registers and read back")
        rq = client.write_registers(1, [10]*8, unit=UNIT)
        rr = client.read_holding_registers(1, 8, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error
        assert(rr.registers == [10]*8)      # test the expected value

        log.debug("Read input registers")
        rr = client.read_input_registers(1, 8, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error

        arguments = {
            'read_address':    1,
            'read_count':      8,
            'write_address':   1,
            'write_registers': [20]*8,
        }
        log.debug("Read write registeres simulataneously")
        rq = client.readwrite_registers(unit=UNIT, **arguments)
        rr = client.read_holding_registers(1, 8, unit=UNIT)
        assert(not rq.isError())     # test that we are not an error
        assert(rq.registers == [20]*8)      # test the expected value
        assert(rr.registers == [20]*8)      # test the expected value
        break
    client.close()


if __name__ == "__main__":
    invokeSyncClient()
    run_sync_client()
