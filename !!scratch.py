import re, json, urllib.request, urllib.error, math, copy

import requests

url = urllib.request.urlopen('http://ddragon.leagueoflegends.com/cdn/10.1.1/data/en_US/champion.json')

data = json.loads(url.read().decode())
for champ, champ_info in data['data'].items():
	print(champ_info['name'], ', ', champ_info['key'])
