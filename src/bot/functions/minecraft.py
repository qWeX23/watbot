import json
from mcstatus import MinecraftServer

if __name__ == "__main__":
    #Load connections config
    with open("../connections.json",'r') as file:
        connections =  json.loads(file.read())
    url = connections['minecraft_ip']+':'+connections['minecraft_port']
    print(url)
    server = MinecraftServer.lookup(url)
    status = server.status()
    print(status)
    print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
    
    print(server_status(None,None))
else:
    #Load connections config
    with open("connections.json",'r') as file:
        connections =  json.loads(file.read())
    async def server_status(args=None,client=None):
        try:
            server = MinecraftServer.lookup(connections['minecraft_ip']+':'+connections['minecraft_port'])
            status = server.status()
            return "the bifrost currently has {} players".format(status.players.online)
        except Exception :
            return "there has been an error, maybe the server is down"


