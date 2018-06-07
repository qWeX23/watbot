print('hello world')
print('start imports')
import asyncio
import datetime
import json
import logging
import pickle
from threading import Thread
import discord
import commands as cmd
from functions import channel
from functions import tz_convert as tz
from functions import minutedata
print('imports done')
print('start logging')
#_________SETUP LOGGING_________
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
#generate filename
log_filename='logs/discord{}.log'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f"))
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#_________END  LOGGING_________
print('log started at {}'.format(log_filename))

#Load connections config
with open("connections.json",'r') as file:
   connections =  json.loads(file.read())

client = discord.Client()

#listens for internal soc connections(DAS)
async def soc_handle(reader, writer):
   
    print('internal listener triggered')
    message = await reader.read(1000000)
    message = pickle.loads(message)
    addr = writer.get_extra_info('peername')
    print(addr)
    if( message['function'] == 'delete_chan'):
       await channel.delete_channel(int(message['chan']),client)
    elif(message['function'] == 'reply_nmt'):
        await client.send_message(message['channel'],message['reply'])
    elif(message['function'] == 'minute_data'):
        writer.write(minutedata.send_data(writer,client))
        await writer.drain()
        writer.close()

#gives streamer role to anyone streaming
#TODO: seperate logic, add dynamic channels to individuals
@client.event
async def on_member_update(before, after):

    # give someone who is streaming streamer role
    member_has_streamer = discord.utils.get(after.roles, name="Streamer")
    streamer_role = discord.utils.get(after.server.roles, name="Streamer")
    if not member_has_streamer and after.game and after.game.type == 1:
        await client.add_roles(after, streamer_role)
    elif member_has_streamer and (not after.game or not after.game.type == 1):
        await client.remove_roles(after, streamer_role)
    #end ===============================


@client.event
async def on_ready():
    #Create internal listener from connections config
    event_loop.create_task(asyncio.start_server(soc_handle, connections['internal_ip'],connections['internal_port'], loop=event_loop))
    #Alive
    print('Logged in as {} working on {}'.format(client.user.name,list(client.servers)[0].name))

#TODO: how can we optimize this?
@client.event
async def on_message(message):

    #watbot sholdn't trigger himself
    if  message.author != client.user:

        #parse all messages for timestamps
        tz_str = tz.parse_and_return(message.content)
        if tz_str is not None:
            await client.send_message(message.channel, "wat? \n {}".format(str(tz_str)))
        
        #parse for command word
        #TODO: configurable commands from a db/ config file
        if message.content.startswith("!"):
            msg_str = await cmd.parse_arguments_and_return(message.content, client)
            await client.send_message(message.channel, msg_str)

        #make an 'intelligent' response to @s
        elif client.user in message.mentions:
            #use static response to internal listener
            reader, writer = await asyncio.open_connection( connections['internal_ip'],connections['internal_port'],loop=event_loop)
            write_message ={
                'message':str(message.content)
                ,'reply':'wat? don\'t @ me' 
                ,'function':'reply_nmt'
                ,'channel':message.channel
            }
            write_message = pickle.dumps(write_message)
            writer.write(write_message)
            writer.close()
        
#sets the event loop for the internal listener
#why not just use client.loop there?
#who knows
#im sure there was a good reason at the time but...
#yep
event_loop = client.loop

#run the client from the connection config
#this is a blocking call
#everything important needs to run before this. 
client.run(connections['client_id'])