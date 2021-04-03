from collections import OrderedDict

from mwcleric.auth_credentials import AuthCredentials
from mwcleric.wiki_client import WikiClient

credentials = AuthCredentials(user_file="wc")
site = WikiClient('https://pcj.fandom.com', credentials=credentials)

variable_to_copy = 'wgCargoPageDataColumns'
from_wiki = 'lol'

wiki_name_to_id_map = {
	"apexlegends-esports": 2294647,
	"cod-esports": 2294030,
	"commons-esports": 2342996,
	"default-loadout-esports": 2293768,
	"help-esports": 2293305,
	"fifa-esports": 2294151,
	# "fortnite-esports": 2294263,
	"gears-esports": 2293557,
	"halo-esports": 2294143,
	"legendsofruneterra-esports": 2295319,
	"lol": 2293615,
	"nba2k-esports": 2293897,
	"paladins-esports": 2293440,
	"pubg-esports": 2293890,
	"rl-esports": 2294760,
	"rollerchampions-esports": 2536304,
	"siege-esports": 2294358,
	"smite-esports": 2293467,
	"splatoon2-esports": 2295280,
	"teamfighttactics": 2295108,
	"valorant-esports": 2295329,
	"vg-esports": 2294444,
	"wildrift-esports": 2415957,
}

print(str(wiki_name_to_id_map[from_wiki]))

token = site.client.get_token('csrf')
result = site.client.api('variableinfo', wiki_id=str(wiki_name_to_id_map[from_wiki]),
                         variable_name=variable_to_copy,
                         token=token)

value_to_set = result['variable_details']['value']
if value_to_set is not None:
	if type(value_to_set) == list:
		value_to_set = '[' + ', '.join(['"{}"'.format(_) for _ in value_to_set]) + ']'
	elif type(value_to_set) == OrderedDict:
		t = []
		for k, v in value_to_set.items():
			if type(v) == str:
				t.append('  "{}": "{}"'.format(k, v))
			
			# wgGrantPermissionsLocal has nested ordered dicts
			elif type(v) == OrderedDict:
				t2 = []
				for k2, v2 in v.items():
					t2.append('    "{}": "{}"'.format(k2, v2))
				# k, v is the outer ordered dict key/value pair
				t.append('  ' + '"{}": '.format(k) + '{\n' + ',\n'.join(t2) + '\n  }')
		value_to_set = '{\n' + ',\n'.join(t) + '\n}'

print('Calculated value: {}'.format(value_to_set))

for to_wiki, to_wiki_id in wiki_name_to_id_map.items():
	if to_wiki == from_wiki:
		continue
	print('Setting {} on {}'.format(variable_to_copy, to_wiki))
	
	old_result = site.client.api('variableinfo', wiki_id=str(to_wiki_id),
	                             variable_name=variable_to_copy,
	                             token=token)
	old_value = old_result['variable_details']['value']
	print(to_wiki, ': ', old_value)
	
	site.client.api('savewikiconfigvariable', wiki_id=str(to_wiki_id), variable_name=variable_to_copy,
	                variable_value=value_to_set, reason="Cloning value from {}".format(from_wiki),
	                token=token)
