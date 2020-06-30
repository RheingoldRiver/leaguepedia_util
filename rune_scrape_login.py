import requests, json

auth = json.load(open('riot_auth.json'))

url = 'https://auth.riotgames.com/token'

data = {
	'client_assertion_type' : 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
	'client_assertion' : 'eyJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29tXC90b2tlbiIsInN1YiI6ImxvbCIsImlzcyI6ImxvbCIsImV4cCI6MTYwMTE1MTIxNCwiaWF0IjoxNTM4MDc5MjE0LCJqdGkiOiIwYzY3OThmNi05YTgyLTQwY2ItOWViOC1lZTY5NjJhOGUyZDcifQ.dfPcFQr4VTZpv8yl1IDKWZz06yy049ANaLt-AKoQ53GpJrdITU3iEUcdfibAh1qFEpvVqWFaUAKbVIxQotT1QvYBgo_bohJkAPJnZa5v0-vHaXysyOHqB9dXrL6CKdn_QtoxjH2k58ZgxGeW6Xsd0kljjDiD4Z0CRR_FW8OVdFoUYh31SX0HidOs1BLBOp6GnJTWh--dcptgJ1ixUBjoXWC1cgEWYfV00-DNsTwer0UI4YN2TDmmSifAtWou3lMbqmiQIsIHaRuDlcZbNEv_b6XuzUhi_lRzYCwE4IKSR-AwX_8mLNBLTVb8QzIJCPR-MGaPL8hKPdprgjxT0m96gw',
	'grant_type' : 'password',
	'username' : auth["username"],
	'password' : auth["password"],
	'scope' : 'openid offline_access lol ban profile email phone'
}

session = requests.Session()

r = session.post(url, data=data)

token = r.json()['id_token']

print(session.get('https://acs.leagueoflegends.com/v1/stats/game/TRLH3/1001090130?gameHash=6d4d5dd0e2fedbbc', cookies = { 'id_token' : token }).json())
