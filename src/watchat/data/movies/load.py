from pymongo import MongoClient
from tqdm import tqdm
import ast

"""
turns a line into a dict
- fields:
		- lineID
		- characterID (who uttered this phrase)
		- movieID
		- character name
		- text of the utterance

"""
def decode_line_lines(line,i):
    parts = line.split('+++$+++')
    parts = [p.strip() for p in parts]
    return {
        'SEQ_NUM':i,
        'LINE_ID':parts[0],
        'CHARACTER_ID':parts[1],
        'MOVIE_ID':parts[2],
        'CHARACTER_NAME':parts[3],
        'UTTERANCE':parts[4]
    }

"""
turns a line into a dict
- fields
		- characterID of the first character involved in the conversation
		- characterID of the second character involved in the conversation
		- movieID of the movie in which the conversation occurred
		- list of the utterances that make the conversation, in chronological 
			order: ['lineID1','lineID2',É,'lineIDN']
			has to be matched with movie_lines.txt to reconstruct the actual content

"""
def decode_line_convs(line,i):
    parts = line.split('+++$+++')
    parts = [p.strip() for p in parts]
    return {
        'SEQ_NUM':i,
        'FIRST_CHARACTER_ID':parts[0],
        'SECOND_CHARACTER_ID':parts[1],
        'MOVIE_ID':parts[2],
        'UTTERANCES':ast.literal_eval(parts[3])
    }



mongo = MongoClient('127.0.0.1',27017)
db = mongo['watchat']
col_convs = db['movie.conversations']
col_lines = db['movie.lines']
col_convs.delete_many({})
col_lines.delete_many({})
with open('movie_lines.txt') as lines:
    i=0
    for line in tqdm(lines):
        col_lines.insert_one(decode_line_lines(line,i))
        i+=1
with open('movie_conversations.txt') as convs:
    i=0
    for line in tqdm(convs):
        col_convs.insert_one(decode_line_convs(line,i))
        i+=1
        
