
# import sys
# sys.path.append( 'nmt-chatbot')
# from inference import inference as inference


# print(inference("hello, how are you"))


import asyncio
import pickle
async def go():
    reader, writer = await asyncio.open_connection('127.0.0.1', 2312, loop=asyncio.get_event_loop())
    writer.write(pickle.dumps({
                'message':'asdasd'
                ,'reply':'wat? don\'t @ me' 
                ,'function':'reply_nmt'
                ,'channel':''''''
            }))

asyncio.get_event_loop().run_until_complete(go())