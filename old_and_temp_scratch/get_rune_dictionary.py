import json, urllib.request

json_loc =

with urllib.request.urlopen('http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/runesReforged.json') as url:
	data= json.loads(url.read().decode())

rune_dict = {}

for tree in data:
	for slot in tree['slots']:
		for rune in slot['runes']:
			rune_dict[rune['id']] = rune['name']

output = []

for key in rune_dict.keys():
	output.append('|{}={}'.format(key, rune_dict[key]))

f = open("runedata.txt", "a")
f.write('\n'.join(output))