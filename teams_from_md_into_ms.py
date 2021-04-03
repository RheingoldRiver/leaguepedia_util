from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials
import urllib.request, json, re, mwparserfromhell

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Adding MH + teams/winner from MH'  # Set summary

limit = -1
startat = -1

thispage = 'LJL/2017 Season/Spring Season'
pages_array = [thispage]

team_replace = {
	'ae' : 'abyss esports',
	'tm' : 'tm gaming'
}

lmt = 0
for pagename in pages_array:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % pagename)
	else:
		page = site.client.pages[pagename + '/Match Details']
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		game_info = []
		for template in wikitext.filter_templates():
			if template.name.matches('MHLink'):
				if template.has('link'):
					md = template.get('link').value.strip()
					if md != '':
						gamelocation = re.findall(r'match-details/(.+?)(?:&tab.*)', md)[0]
						
						with urllib.request.urlopen("https://acs.leagueoflegends.com/v1/stats/game/" + gamelocation) as url:
							data = json.loads(url.read().decode())
						
						name = data['participantIdentities'][0]['player']['summonerName']
						blue = re.findall(r'^(.+?) ', name)[0]
						
						name = data['participantIdentities'][5]['player']['summonerName']
						red = re.findall(r'^(.+?) ', name)[0]
						
						if blue.lower() in team_replace:
							blue = team_replace[blue.lower()]
						if red.lower() in team_replace:
							red = team_replace[red.lower()]
						
						winner = 1 if data['teams'][0]['win'] == 'Win' else 2
						game_info.append({'blue' : blue, 'red' : red, 'winner' : str(winner), 'mh' : md})
					else:
						game_info.append({'blue': '', 'red' : '', 'winner' : '', 'mh' : ''})
		
		data_page = site.client.pages['Data:' + pagename]
		data_text = data_page.text()
		data_wikitext = mwparserfromhell.parse(data_text)
		
		i = 0
		for template in data_wikitext.filter_templates():
			if template.name.matches('MatchSchedule/Game'):
				if template.has('ff') and template.get('ff').value.strip() in ['1', '2']:
					pass
				else:
					template.add('blue', game_info[i]['blue'])
					template.add('red', game_info[i]['red'])
					template.add('winner', game_info[i]['winner'])
					template.add('mh', game_info[i]['mh'])
					i = i + 1
		
		data_text_new = str(data_wikitext)
		if data_text_new != text:
			print('Saving page %s...' % data_page.name)
			data_page.save(data_text_new, summary=summary)
		else:
			print('Skipping page %s...' % data_page.name)

