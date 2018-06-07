import pytz
from pytz import timezone
import time
from datetime import datetime
import re


def parse_and_return(message):
    ts = find_timestamps(message)
    if not ts:
        return None
    else:
        #print("retrun str: {}".format(all_zones(extract_time(ts))))
        return all_zones(extract_time(ts))

def find_timestamps(input):
    #print(input)
    pattern = re.compile('\d*\d:*\d*\d*[pa]*[m]* *[ecmp][sd][t]')
    return re.findall(pattern,input)
    
def extract_time(time):
    #TODO: make dynamic for multiple timestamps per message
    time=str(time)
    
    #find numbers
    pattern = re.compile('\d{1,2}')
    time_numbers = [int(x) for x in re.findall(pattern,time)]
    
    #find am-pm
    pattern = re.compile('[pa][m]')
    ampm = re.findall(pattern, time)
    
    #converts to 24hr
    if any('p' in x for x in ampm) and '12' not in str(time_numbers[0]):
        time_numbers[0]+=12
    elif any('a' in x for x in ampm) and '12' in str(time_numbers[0]) and time_numbers[0] >= 12:
        time_numbers[0]-=12
        
    #find TZ
    pattern = re.compile('[ecmp][sd][t]')
    tz = re.findall(pattern, time)[0]
    #map to timezone
    tzz = ''
    if 'e' in tz:
        tzz = timezone('US/Eastern')
    elif 'c' in tz:
        tzz = timezone('US/Central')
    elif 'm' in tz:
        tzz = timezone('US/Mountain')
    elif 'p' in tz:
        tzz = timezone('US/Pacific')
    
    return tzz.localize(datetime(1994,4,27,int(time_numbers[0]),int(time_numbers[1])))
    
        
def convert_timestamps(times):
    return [extract_time(time) for time in times]
        
def all_zones(time):
    fmt = '%H:%M %Z%z'
    e = timezone('US/Eastern')
    c = timezone('US/Central')
    m = timezone('US/Mountain')
    p = timezone('US/Pacific')
    return (time.astimezone(e).strftime(fmt),time.astimezone(c).strftime(fmt),time.astimezone(m).strftime(fmt),time.astimezone(p).strftime(fmt))   