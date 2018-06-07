import json

import pyowm

with open('connections.json','r') as file:
    connections =  json.loads(file.read())
    owm = pyowm.OWM(connections['owm_key'])


"""
This function parses the command and calls the appropriate API Call
"""
async def parse_args(args, client=None):
    name = ' '.join(args)
    w = await get_weather(name)
    if w is not None:
        return "it is {} degrees with {} in {}".format(w[0],w[1],name)
    else:
        return "there has been an error"

"""
Gets weather data by name of place, aso works with zip
"""
async def get_weather(place):
    try:
        obs = owm.weather_at_place(place)
        w = obs.get_weather()
        return (w.get_temperature('fahrenheit')['temp'],w.get_detailed_status())
    except:
        return None

