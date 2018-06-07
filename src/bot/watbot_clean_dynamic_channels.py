import discord
from pymongo import MongoClient
import json
from datetime import datetime
from datetime import timedelta
from functions import channel
import asyncio
import pickle


async def main():
    with open("connections.json",'r') as file:
        connections =  json.loads(file.read())
    #init DB
    mongo = MongoClient(connections['mongo_ip'], connections['mongo_port'])
    db = mongo['watbot']
    chan_col = db['dynamic_channels']
    #set up socket sorcery
    loop = asyncio.get_event_loop()
    #send a message for all expired channels
    for chan in chan_col.find({'expiration_date':{"$lt":int(datetime.now().strftime("%Y%m%d"))}}):
        print(chan)
        reader, writer = await asyncio.open_connection(connections['internal_ip'], connections['internal_port'], loop=loop)
        writer.write(pickle.dumps({'function':'delete_chan','chan':chan['id']}))
    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
