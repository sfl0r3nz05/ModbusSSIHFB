#!/usr/bin/env python
from pymodbus.server.sync import StartTlsServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer

def run_server():
    server_cert = 'server.crt'
    server_key = 'privk.key'
    cafile_cert = '../modbus-sync-client/client.crt'
    did_wallet_path = "walletDid.json"

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

    StartTlsServer(context, identity=identity, address=("0.0.0.0", 8020), certfile=server_cert, keyfile=server_key, cafile=cafile_cert, did_wallet_path=did_wallet_path)

if __name__ == "__main__":
    run_server()
