"""
Function to take the arguments given to watbot and
then excecute commands
"""

from collections import defaultdict
import sys
import re

#import the functions we interact with
from functions import poll
from functions import channel
from functions import weather
from functions import giphy
from functions import minecraft
from functions import dota

#function to call when there are no arguments found
def no_command_found():
    return 'Not a command. Type !help to get help with watbot'

#dictinary object of commands
commands = {
    'poll' : poll.make_poll
    ,'chan' : channel.create_channel
    ,'weather' :weather.parse_args
    ,'gif': giphy.get_gifs
    ,'minecraft':minecraft.server_status
    ,'dota':dota.get_match
}

#function to print commands when someone needs help
async def help_watbot(args,client=None):
    help_text = "Possible Commands:"
    for x in commands:
        help_text += "\n" + x
    return help_text

#adds the help command after it is defined
commands['help'] = help_watbot

#parses the arguments and then return the function called with the passed arguments
async def parse_arguments_and_return(message,client):
    message_components = re.sub("[!]",'',message).split(' ')
    try:
        dict_function_ref = commands[message_components[0]]
        if len(message_components)>=1:
            return await dict_function_ref(message_components[1:],client)
        else:
            return await dict_function_ref(None,client)
            
    except:
        print("Unexpected error:")
        [print(er) for er in sys.exc_info()]
        return no_command_found()
