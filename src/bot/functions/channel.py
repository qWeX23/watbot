import discord
from pymongo import MongoClient
import json
from datetime import datetime
from datetime import timedelta

with open("connections.json",'r') as file:
   connections =  json.loads(file.read())

mongo = MongoClient(connections['mongo_ip'], connections['mongo_port'])
db = mongo['watbot']
chan_col = db['dynamic_channels']

async def create_channel(message_str, client):
    #parse args
    chan_type = message_str[0]
    chan_name = message_str[1]
    #create channel
    created_chan = await client.create_channel(list(client.servers)[0], chan_name, type=chan_type)
    #update db
    exp_date = datetime.now() + timedelta(days=7)
    exp_date = int(exp_date.strftime("%Y%m%d"))
    chan_col.insert_one({
        'name' : created_chan.name,
        'id' : created_chan.id,
        'expiration_date' : exp_date
    })
        
    return "done"

async def delete_channel(chan_id, client):
    print('searching for chan to delete')
    print(chan_id)
    chan = list(client.servers)[0].get_channel(str(chan_id))
    print('this is the chan found')
    print(chan)
    if chan:
        done = await client.delete_channel(chan)
        print(done)
    return "done"