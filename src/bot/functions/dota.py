
import json
import requests
import pprint

players = [{
	'dotaid':51567556,
	'discordid':120669265681448960
	},
	{
		'dotaid':106748142,
		'discordid':166691671818371072
	}]

match_ids = []

for player in players:
	r = requests.get('https://api.opendota.com/api/players/{}/recentMatches'.format(player['dotaid']))
	matches = json.loads(r.content)
	matchid = matches[0]['match_id']
	print(matchid)
	match_ids.append(matchid)




r= requests.get('https://api.opendota.com/api/matches/{}'.format(max(match_ids)))
print(r.content)

match = json.loads(r.content)
pprint.pprint(match)
with open('match.json', 'w') as filer:
	json.dump(match,filer)

r= requests.get('https://api.opendota.com/api/heroes')
heroes = json.loads(r.content)
with open('heroes.json', 'w') as filer:
	json.dump(heroes,filer)