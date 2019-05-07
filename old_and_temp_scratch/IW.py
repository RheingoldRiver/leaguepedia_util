import requests

username = 'RheingoldRiver@Python'
with open('password.txt') as f:
	password = f.read()
api_url = 'https://vg-esports.gamepedia.com/api.php'

session = requests.Session()

r1 = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
})
r1.raise_for_status()

# get login token
r1 = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
})
r1.raise_for_status()

# log in
r2 = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': r1.json()['query']['tokens']['logintoken'],
})
if r2.json()['login']['result'] != 'Success':
	raise RuntimeError(r2.json()['login']['reason'])

# get edit token
r3 = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
})

token = r3.json()['query']['tokens']['csrftoken']

r = session.post('https://vg-esports.gamepedia.com/index.php?title=Special:Interwiki&action=submit',
				  data = { 'wpInterwikiURL':'https://realmroyale-esports.gamepedia.com/$1',
						   'wpInterwikiPrefix':'realm',
						   'wpEditToken':token,
						   'wpInterwikiAction':'add'
						   },
				  auth = (username, password)
				  )

print(r.text)