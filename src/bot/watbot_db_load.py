import json
import discord
import asyncio
import time
import datetime
from threading import Thread
#import watbot_functions as watbot
from db import db_helper as dbh
from module_bin import tz_convert as tz

from pymongo import MongoClient
from bson import BSON


with open("connections.json",'r') as file:
   connections =  json.loads(file.read())
   print(connections)

mongo = MongoClient(connections['mongo_ip'], connections['mongo_port'])
client = discord.Client()


async def soc_handle(reader, writer):
    return


@client.event
async def on_member_update(before, after):
    return

@client.event
async def on_ready():
    

    #establish db
    db = mongo['watbot']
    #get collections
    mems = db['mems']
    roles = db['roles']
    chans = db['chans']
    #clear collections
    mems.delete_many({})
    roles.delete_many({})
    chans.delete_many({})
    #get current data
    [mems.insert_one(mem)   for mem in dbh.members_to_dict(list(client.servers)[0].members)]
    [roles.insert_one(role) for role in dbh.members_to_dict(list(client.servers)[0].roles)]
    [chans.insert_one(chan) for chan in dbh.members_to_dict(list(client.servers)[0].channels,True)]
    print("Logged in, working....")


@client.event
async def on_message(message):
    return

event_loop = client.loop


client.run(connections['client_id'])