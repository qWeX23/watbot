import asyncio
from PIL import Image
from PIL import ImageGrab

downsize = 480, 270


def take_screencap():
    img = ImageGrab.grab()
    img.thumbnail(downsize)
    img = img.tobytes()
    return img


async def task_get_img(loop):
    while True:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)
        print("sending message")
        writer.write(take_screencap())
        await asyncio.sleep(.5)
        writer.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(task_get_img(loop))
loop.close()
