import pickle
import asyncio


def send_data(socketWriter,client):
    mems = []
    for mem in list(list(client.servers)[0].members):
        obj={
            'discord_id' : mem.id,
            'discord_name' :mem.name,
            'discriminator':mem.discriminator,
            'game' : mem.game.name if mem.game is not None else 'No Game',
            'status' : str(mem.status)
        }
        mems.append(obj)
    p = pickle.dumps(mems)
    return p 