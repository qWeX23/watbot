from sqlalchemy import Column,Integer,String,ForeignKey,ForeignKeyConstraint,BigInteger,DateTime,create_engine,orm
from sqlalchemy.ext.declarative import declarative_base

import pickle
import asyncio
import json

Base = declarative_base()
#DB Models
class Status(Base):
    __tablename__='Status'

    ID = Column(Integer,primary_key=True)
    Status = Column(String)

class Game(Base):
    __tablename__ = 'Game'

    ID=Column(Integer,primary_key=True)
    Game = Column(String)

class User(Base):
    __tablename__ = 'User'

    ID=Column(Integer,primary_key=True)
    DiscordID = Column(String)
    DiscordName = Column(String)
    Discriminator = Column(Integer)

class MinuteData(Base):
    __tablename__ = 'MinuteData'

    ID=Column(BigInteger,primary_key=True)
    Status = Column(ForeignKey('Status.ID'))
    Game = Column(ForeignKey('Game.ID'))
    User = Column(ForeignKey('User.ID'))
    InsertDateTime = Column(DateTime)

#Configure engine and create session
with open("../bot/connections.json",'r') as file:
    c =  json.loads(file.read())
    connectionString = "mysql://"+c['sql_user']+":"+c['sql_pass']+"@"+c['sql_host']+"/"+c['sql_db']

engine = create_engine(connectionString)

Base.metadata.bind = engine      
Base.metadata.create_all()

sesMaker = orm.sessionmaker()
sesMaker.configure(bind = engine)
ses=sesMaker()

# resuly = ses.execute(MinuteData.select())
ses.add(Status(Status='idle'))

stautses = ses.query(Status).all()
for s in stautses:
    print (s.Status)



