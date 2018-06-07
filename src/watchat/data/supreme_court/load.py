from pymongo import MongoClient
from tqdm import tqdm

"""
turns a line into a dict

CASE_ID +++$+++ UTTERANCE_ID +++$+++ AFTER_PREVIOUS +++$+++ 
SPEAKER +++$+++ IS_JUSTICE +++$+++ JUSTICE_VOTE +++$+++ 
PRESENTATION_SIDE +++$+++ UTTERANCE

"""
def decode_line(line,i):
    parts = line.split('+++$+++')
    parts = [p.strip() for p in parts]
    return {
        'SEQ_NUM':i,
        'CASE_ID':parts[0],
        'UTTERANCE_ID':parts[1],
        'AFTER_PREVIOUS':parts[2],
        'SPEAKER':parts[3],
        'IS_JUSTICE':parts[4],
        'JUSTICE_VOTE':parts[5],
        'PRESENTATION_SIDE':parts[6],
        'UTTERANCE':parts[7],
    }


mongo = MongoClient('127.0.0.1',27017)
db = mongo['watchat']
col = db['supreme.conversations']
col.delete_many({})
with open('supreme.conversations.txt') as convs:
    i=0
    for line in tqdm(convs):
        col.insert_one(decode_line(line,i))
        i+=1
        
