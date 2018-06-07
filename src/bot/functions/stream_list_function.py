"""
function definition for calling the list of streams from the
listed streamers
"""

from api_helpers import twitch

global t
t = twitch.streams()
t.start()

def fill_white_space(max_len,used_len):
    return ''.join([' ' for x in range(max_len-used_len)])
def format_top(line_len):
    return ''.join(['_' for x in range(line_len)])


def format_streams_message(channels, status):
    #TODO: REFACTOR!
    status=['OFFLINE' if x is None else x for x in status]
    message = "W_ A _T"
    max_len_channels = len(max(channels, key=len))
    max_len_status = len(max(status, key=len))
    line_len = max_len_status+max_len_channels+5
    #print (max_len_channels)
    #print(max_len_status)
    #print(line_len)
    message = message+"\n   "
    message = message+format_top(line_len)
    for channel,stat in zip(channels,status):
        message = message+"\n   |"
        message= message +channel
        message = message + fill_white_space(max_len_channels,len(channel))
        message= message+" |"
        if stat not in '':
            message = message + stat
            message = message +fill_white_space(max_len_status,len(stat)) +" |"
        else:
            message = message +fill_white_space(max_len_status,len(stat))+" |"
        message = message+"\n   "
        message = message +''.join(['-' for x in range(line_len)])
    message = message+"\n   "
    # message = message+format_top(line_len)
    return "`"+message+"`"

def list_twitch_streams(args):
    return "W A T \n {} ".format(format_streams_message(t.channels,t.status))
