import pickle
import json
import time
import asyncio
import MySQLdb
import re
import datetime
import sys
import logging

with open("../bot/connections.json",'r') as file:
    connections =  json.loads(file.read())

host= connections['sql_host']
user = connections['sql_user']
passwd = connections['sql_pass']

db = MySQLdb.connect(host=host,user=user,passwd=passwd,db="watbot")
def upsert_user(record):
    #upsert users
        cur = db.cursor()
        query = """
        INSERT INTO User (DiscordID,DiscordName,Discriminator) 
        VALUES ("{0}","{1}",{2})
        ON DUPLICATE KEY UPDATE 
        DiscordID="{0}",
        DiscordName="{1}",
        Discriminator={2};
        """.format(clean(record['discord_id']),clean(record['discord_name']),record['discriminator'])
        cur.execute(query)
        db.commit()

def upsert_game(record):
    #upsert users
        cur = db.cursor()
        query = """
        INSERT INTO Game (Game) 
        VALUES ("{0}")
        ON DUPLICATE KEY UPDATE 
        Game ="{0}"
        """.format(clean(record['game']))
        cur.execute(query)
        db.commit()

def upsert_status(record):
      #upsert status
      cur = db.cursor()
      query = """
      INSERT INTO Status (Status) 
      VALUES ("{0}")
      ON DUPLICATE KEY UPDATE 
      Status ="{0}"
      """.format(clean(record['status']))
      cur.execute(query)
      db.commit()

def insert_data(record,current_time):
    cur = db.cursor()
    query="""
    INSERT INTO MinuteData
    (Status,Game,User,InsertDateTime)
    SELECT s.ID,g.ID,u.ID,"{3}"
    FROM Status s
    JOIN Game g ON g.Game = "{0}"
    JOIN User u on u.DiscordID = "{1}"
    WHERE s.Status = "{2}"
    """.format(clean(record['game']),clean(record['discord_id']),clean(record['status']),str(current_time))
    cur.execute(query)
    db.commit()

def write_to_db(data):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for record in data:
        upsert_user(record)
        upsert_game(record)
        upsert_status(record)
        insert_data(record,current_time)
    pass

def clean(data):
   return re.compile('[\W_]+').sub('', data)
    

async def data_getter(loop):
    #_________SETUP LOGGING_________
    logger = logging.getLogger('minute_data')
    logger.setLevel(logging.DEBUG)
    #generate filename
    log_filename='logs/discord{}.log'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f"))
    handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    #_________END  LOGGING_________
    while 1==1:
        try:
            reader, writer = await asyncio.open_connection(host=connections['external_ip'],port=connections['external_port'],loop=loop)
            message = {'function':'minute_data'} 
            data = pickle.dumps(message)
            writer.write(data)
            data = await reader.read()
            message = pickle.loads(data)
            print(message)
            writer.close()
            write_to_db(message)
        except:
            logger.debug([er for er in sys.exc_info()])
        finally:
            await asyncio.sleep(60)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(data_getter(loop))
loop.close()