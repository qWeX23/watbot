import requests
import json
import threading
import time
import asyncio

class streams(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self,group=None,target=None,name="twitch.streams thread")
        self.streamurl="https://api.twitch.tv/kraken/streams/"
        self.headers = {
            'Client-ID': 'el875mi01rju61h7x39vs450txrthu'
        }
        url = 'https://api.twitch.tv/kraken/streams/wezi0'
        self.status = "Nothing"
        self.daemon = True
        #TODO: read channels form file/db
        self.channels = ["summit1g","wezi0","tzfy","timthetatman"]
        self.status = [None for x in self.channels]

    def run(self):
        print("Starting Twitch listener")
        while True:
            self.status = [self.get_status(channel) for channel in self.channels]
            #print(self.status)
            for x in range(60):
                time.sleep(1) #only poll twitch every minute

    def get_status(self, channel):
            r = requests.get(self.streamurl+channel,headers=self.headers)
            j = r.json()
            if(j['stream']==None):
                return None
            else:
                return j['stream']['channel']['url']

# get_stream_status("wezi0")
