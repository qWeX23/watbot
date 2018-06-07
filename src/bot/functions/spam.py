import random 
import asyncio

async def spam_wat(client,channel):
    num_wats = int(abs(random.normalvariate(1,4)))+1
    delay = random.uniform(1,5)
    for i in range(0,num_wats):
        await asyncio.sleep(delay)
        await client.send_message(channel,"wat",tts=True)