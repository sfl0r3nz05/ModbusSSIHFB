#!/usr/bin/env python
from app.HFBapp.invokeSyncServer import invokeSyncServer
from app.HFBapp.querySyncServer import querySyncServer
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartTlsServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.server.sync import MyModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import os
import socket
import hashlib
import base64
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)


def run_sync_client():
    response = querySyncServer()
    message = b"Client"
    message = base64.b64encode(hashlib.sha256(message).digest())
    message = message.decode("utf-8")
    if message != response['hash']:
        return False
    else:
        return True


def run_server():
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17]*100),
        ir=ModbusSequentialDataBlock(0, [17]*100))
    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    response = querySyncServer()
    _logger.debug("Query Server response %s" % response)

    StartTcpServer(context, identity=identity, address=(
        "192.168.192.2", 5020), response=response['hash'])


if __name__ == "__main__":
    invokeSyncServer()
    aut = True
    if aut == True:
        run_server()
    else:
        print("Error en autenticacion")
