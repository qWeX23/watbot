from pymongo import MongoClient
from tqdm import tqdm
import os

froms = open('movies.from','w')
tos = open('movies.to','w')

def parse_utterances(a):
    max_i = len(a)-1
    dialog_pairs =[]
    for i in range(0,max_i,2):
        if i == max_i:
            return
        else:
            dialog_pairs.append((a[i],a[i+1]))
    save_pair(dialog_pairs)
        

def save_pair(pairs):

    for pair in pairs:
        froms.write(pair[0]+'\n')
        tos.write(pair[1]+'\n')

mongo = MongoClient('127.0.0.1',27017)
db = mongo['watchat']
col_convs = db['movie.conversations']
col_lines = db['movie.lines']

conversations = []
for doc in tqdm(col_convs.find({},{'_id':0,'UTTERANCES':1})):
    utterances = [col_lines.find_one({"LINE_ID":utterance},{'_id':0,'UTTERANCE':1})['UTTERANCE'] for utterance in doc['UTTERANCES']]
    utterances = [bytes(line, 'utf-8').decode('utf-8', 'ignore') for line in utterances]
    parse_utterances(utterances)   

froms.close()
tos.close()