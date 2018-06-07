import asyncio
from PIL import Image


def process_image():
    # do detector things
    print("processing image!")


async def send_to_watbot():
    reader, writer = await asyncio.open_connection('127.0.0.1', 23120, loop=loop)
    print("sending message")
    writer.write("Hello Watbot".encode())
    writer.close()


async def soc_handle(reader, writer):
    print("message received")
    message = await reader.read()
    img = Image.frombytes('RGB', (480, 270), message)
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % ("img", addr))
    process_image()
    await send_to_watbot()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(soc_handle, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
