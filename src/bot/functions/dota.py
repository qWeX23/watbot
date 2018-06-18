
import json
import requests
from prettytable import PrettyTable

with open('heroes.json') as hf:
	heroes = json.load(hf)
	hf.close()

async def get_match(id,client=None):
	r= requests.get('https://api.opendota.com/api/matches/{}'.format(id[0]))
	match = json.loads(r.content)
	if 'error' in match:
		return match['error']
	else:
		return "```{}```".format(format_match(match))


def format_match(match):
	t = PrettyTable(['player','hero','gpm','xpm','kda'])

	for player in match['players']:
		row = []
		if 'personaname' in player:
			row.append(player['personaname'])
		else:
			row.append(None)
		row.append(next((hero['localized_name'] for hero in heroes if hero['id'] == player['hero_id'])))
		row.append(player['gold_per_min'])
		row.append(player['xp_per_min'])
		row.append(player['kda'])
		t.add_row(row)
	t.hrules=False
	t.align = 'l'
	t.horizontal_char ='='
	return t

# players = [{
# 	'dotaid':51567556,
# 	'discordid':120669265681448960
# 	},
# 	{
# 		'dotaid':106748142,
# 		'discordid':166691671818371072
# 	}]

# match_ids = []

# for player in players:
# 	r = requests.get('https://api.opendota.com/api/players/{}/recentMatches'.format(player['dotaid']))
# 	matches = json.loads(r.content)
# 	matchid = matches[0]['match_id']
# 	print(matchid)
# 	match_ids.append(matchid)




# r= requests.get('https://api.opendota.com/api/matches/{}'.format(max(match_ids)))
# print(r.content)

# match = json.loads(r.content)
# pprint.pprint(match)
# with open('match.json', 'w') as filer:
# 	json.dump(match,filer)

