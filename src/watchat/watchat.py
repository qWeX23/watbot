import pickle
import asyncio
import json
import re
import sys
sys.path.append( 'nmt-chatbot')
from inference import inference as inference


#with open("connections.dict",'r') as file:
#    connections =  json.loads(file.read())

def process_message(message):
    #send to nmt
    re.sub('<[^>]+>', '', message)
    return inference(message)['answers'][0]


async def send_to_watbot(command):
    reader, writer = await asyncio.open_connection('127.0.0.1', 2312, loop=loop)
    print("sending message")
    writer.write(pickle.dumps(command))
    writer.close()

"""
Takes a message from watbot and processes the reply. is the coro for internal server. 

{
    'message': message from watbot
    'reply': reply from the nmt
    'function': reply_nmt
    'channel' channel for watbot to reply into
}
"""
async def soc_handle(reader, writer):
    print("message received")
    command = await reader.read()
    command = pickle.loads(command)
    command['reply'] = process_message(command['message'])
    await send_to_watbot(command)
   


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



