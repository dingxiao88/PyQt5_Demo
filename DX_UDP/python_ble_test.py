# import BLE_GATT

# ubit_address = 'E5:10:5E:37:11:2d'
# led_text = 'e95d93ee-251d-470a-a062-fa1922dfa9A8'
# led_matrix_state = 'e95d7b77-251d-470a-a062-fa1922dfa9a8'

# ubit = BLE_GATT.Central(ubit_address)
# ubit.connect()
# ubit.char_write(led_text, b'test')
# ubit.char_write(led_matrix_state, [1, 2, 4, 8, 16])
# print(ubit.char_read(led_matrix_state))
# ubit.disconnect()

# ------------------------------ok---------------------------
# import bluetooth

# nearby_devices = bluetooth.discover_devices(lookup_names=True)

# for addr, name in nearby_devices:
#     print("add:", addr)
#     print("name:", name)






# import asyncio
# from bleak import BleakScanner

# async def run():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

# ------------------------------ok---------------------------

# 9C:9C:1F:C7:66:12
# beb5483e-36e1-4688-b7f5-ea07361b26a8  --server
# 4fafc201-1fb5-459e-8fcc-c5c9c331914b

# from bleak import BleakClient
# import asyncio

# temperatureUUID = "45366e80-cf3a-11e1-9ab4-0002a5d5c51b"
# ecgUUID = "46366e80-cf3a-11e1-9ab4-0002a5d5c51b"

# # notify_uuid = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(0xFFE1)

# notify_uuid =  "beb5483e-36e1-4688-b7f5-ea07361b26a8"


# def callback(sender, data):
#     # print(sender, data)
#     print("---->date")


# def run(addresses):
#     loop = asyncio.get_event_loop()

#     tasks = asyncio.gather(*(connect_to_device(address) for address in addresses))

#     loop.run_until_complete(tasks)


# async def connect_to_device(address):
#     print("starting", address, "loop")
#     async with BleakClient(address, timeout=5.0) as client:

#         print("connect to", address)
#         try:
#             # await client.start_notify(notify_uuid, callback)
#             # await asyncio.sleep(20.0)
#             # await client.stop_notify(notify_uuid)

#             client.write_gatt_char(notify_uuid, b"\x55")
#             await asyncio.sleep(1.0)
#         except Exception as e:
#             print(e)

#     print("disconnect from", address)


# if __name__ == "__main__":
#     # run(
#     #     ["9C:9C:1F:C7:66:12", "beb5483e-36e1-4688-b7f5-ea07361b26a8"]
#     # )
#     run(
#         ["9C:9C:1F:C7:66:12"]
#     )


# ------------------------------ok---------------------------

import asyncio
from bleak import BleakClient

# address = "9C:9C:1F:C7:66:12"
address = "A4:CF:12:73:44:02"
UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

def convert_rgb(rgb):
    scale = 0xFF
    adjusted = [max(1, chan) for chan in rgb]
    total = sum(adjusted)
    adjusted = [int(round(chan / total * scale)) for chan in adjusted]

    # Unknown, Red, Blue, Green
    return bytearray([0x1, adjusted[0], adjusted[2], adjusted[1]])


async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        # print("Connected: {0}".format(x))
        while(1):
            y = await client.read_gatt_char(UUID)
            print(y[0])
            color = convert_rgb([255, 0, 0])
            await client.write_gatt_char(UUID, b"\x01")
            await asyncio.sleep(1.0)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))