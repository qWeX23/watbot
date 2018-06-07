from pymongo import MongoClient
import pymongo
from tqdm import tqdm
import os

def save(pairs):
    froms = open('movies.from','w')
    tos = open('movies.to','w')
    for pair in pairs:
        froms.write(pair[0]+'\n')
        tos.write(pair[1]+'\n')
    froms.close()
    tos.close()

mongo = MongoClient('127.0.0.1',27017)
db = mongo['watchat']
col_convs = db['supreme.conversations']

#find all of the case IDs
conv_ids = col_convs.distinct("CASE_ID")

seq_num=0
dialog_pairs=[]

for c in tqdm(conv_ids):
    convs = list(col_convs.find({"CASE_ID":c},{"_id":0,"CASE_ID":1,"SEQ_NUM":1,"UTTERANCE":1}).sort("SEQ_NUM",pymongo.ASCENDING))
    max_i = len(convs)-1
    for i in range(0,max_i,2):
        if i == max_i:
            break
        else:
            dialog_pairs.append((convs[i]['UTTERANCE'],convs[i+1]['UTTERANCE']))
    save(dialog_pairs)