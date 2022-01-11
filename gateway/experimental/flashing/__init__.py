import asyncio
from binascii import hexlify, crc32
from bleak import BleakScanner
from bleak import BleakClient
import time
from gateway import sensor
import logging

loop = asyncio.get_event_loop()

# Creat a named logger 'log' and set it on INFO level
log = logging.getLogger('SensorGatewayBleak')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

interface = sensor.sensor_interface

fh = FutureHolder()

class ErrorBootloaderModus(Exception):
    """Raised when the sensor is not in bootloader modus

    Args:
        Exception (Custom): "sensor is not in bootloader modus"
    """    
    pass

class FutureHolder:
    furure = None

    def __init__(self):
        self.reset()
    
    async def wait(self):
        await self.furure

    def reset(self):
        self.future=loop.create_future()
    
    def set_result(self, result):
        self.future.set_result(result)
    
    def set_exception(self, exception):
        self.future.set_exception(exception)

    def result(self):
        return self.furure.result()

class device_firmware_upgrade(s1 = sensor.sensor):
    def __init__(self):
        self.sensor = s1

    def check_boot_loader(self):
        if "RuuviBoot" in self.sensor.name:
            log.info("sensor is in bootloader modus")
            return
        elif "DEFAULT" in self.sensor.name:
            raise AttributeError("device_firmware_upgrade can't run with 'default' name")
        else:
            raise ErrorBootloaderModus("sensor is not in bootloader modus")
    
    async def sendPaket(client, c, data):
        fh.reset()
        await client.write_gatt_char(c, data)
        await fh.wait()
        return fh.result()
    
    async def sendData(self, client, obj, data):
        log.info("excecute select...")
        result = await self.sendPaket(client, DFU_CONTROL_POINT, bytearray.fromhex("06%02x"%(obj))) #DFU_CONTROL aus interface!
        offset = result["offset"]
        crc = result["crc32"]
        max_size = result["max_size"]
        if offset<len(data):
            log.info("create sending...")
            blocklen = len(data)
            if blocklen>max_size:
                blocklen=max_size
            msg = bytearray.fromhex("01%02x"%(obj))
            msg.extend(int.to_bytes(blocklen, 4, byteorder="little", signed=False))
            result = await self.sendPaket(client, DFU_CONTROL_POINT, msg)

            log.info("data sending...")
            bytecount = 0
            globalbytecount = 0
            for i in range(offset, len(data), 16):
                ende=i+16
                if ende > len(data):
                    ende= len(data)
                msg = data[i:ende]
                await client.write_gatt_char(DFU_DATA, msg)
                crc = crc32(msg, crc)
                bytecount += len(msg)

                if bytecount+len(msg)>max_size:
                    globalbytecount += bytecount
                    bytecount = 0
                    log.info("execute for {} bytes".format(globalbytecount))
                    msg = bytearray.fromhex("04")
                    result = await self.sendPaket(client, DFU_CONTROL_POINT, msg)

                    blocklen = len(data)-globalbytecount
                    if blocklen>max_size:
                        blocklen = max_size
                    msg = bytearray.fromhex("01%02x" %(obj))
                    msg.extend(int.to_bytes(blocklen, 4, byteorder='little', signed=False))
                    result = await self.sendPaket(client, DFU_CONTROL_POINT, msg)
        log.info("request crc")
        msg = bytearray.fromhex("03")
        result = await self.sendPaket(client, DFU_CONTROL_POIN, msg)
        if result["crc32"]!=crc32(data):
            raise Exception("crc values don't match to each other!")
        else:
            log.info("data send successful")
        log.info("execute...")
        msg = bytearray.fromhex("04")
        result = await self.sendPaket(client, DFU_CONTROL_POINT , msg)

    async def updateProcedure(adress):
        print("lorem ipsum")
    


    def callback(sender : int, value: bytearray):
        value = value[1:]
        if value[1]==0x01:
            if value[0]==0x06:
                fh.set_result({
                    "max_size": int.from_bytes(value[2:6], byteorder='little', signed=False),
                    "offset": int.from_bytes(value[6:10], byteorder='little', signed=False),
                    "crc32": int.from_bytes(value[10:14], byteorder='little', signed=False)
                })
            elif value[0]==0x03:
                fh.set_result({
                    "offset": int.from_bytes(value[2:6], byteorder='little', signed=False),
                    "crc32": int.from_bytes(value[6:10], byteorder='little', signed=False)                    
                })
            elif value[0]==0x01 or value[0]==0x02 or value[0]==0x04:
                fh.set_result(None)
            else:
                fh.future.set_exception(Exception("unknown message"))
        elif value[1]==0x00: #NRF_DFU_RES_CODE_INVALID
            fh.set_exception(Exception("invalid opcode!"))
        elif value[1]==0x02: #NRF_DFU_RES_CODE_OP_NOT_SUPPORTED
            fh.set_exception(Exception("opcode not supported!"))
        elif value[1]==0x03: #NRF_DFU_RES_CODE_INVALID_PARAMETER
            fh.set_exception(Exception("missing or invalid parameter value!"))
        elif value[1]==0x04: #NRF_DFU_RES_CODE_INSUFFICIENT_RESOURCES
            fh.set_exception(Exception("not enough memory for the data object"))
        elif value[1]==0x05: #NRF_DFU_RES_CODE_INVALID_OBJECT
            fh.set_exception(Exception("data object does not match to the firmware and hardware requirements, the signature is wrong, or parsing the command faild!"))
        elif value[1]==0x07: #NRF_DFU_RES_CODE_UNSUPPORTED_TYPE
            fh.set_exception(Exception("not a valid object type for a create request!"))
        elif value[1]==0x08: #NRF_DFU_RES_CODE_OPERATION_NOT_PERMITTED
            fh.set_exception(Exception("the state of the DFU process does not allow this operation!"))
        elif value[1]==0x0a: #NRF_DFU_RES_CODE_OPERATION_FAILD
            fh.set_exception(Exception("operation faild!"))
        elif value[1]==0x0b: #NRF_DFU_RES_CODE_EXT_ERROR
            fh.set_exception(Exception("extended error. The next byte of the response contains the error code of the extended error!"))

