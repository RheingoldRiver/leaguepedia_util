import mwparserfromhell
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

summary = 'Semi-automatically migrating MD pages to Data namespace (Python)'
credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
limit = -1
startat = -1

# pagename = 'OPL/2018 Season/Split 1'
# pages_var = [pagename]

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages_var = [page.strip() for page in pages]

param_lookup = {
	"team1" : "blue",
	"team2" : "red",
	"pb" : "vodpb",
	"gamestart" : "vodstart",
	"post" : "vodpost",
	"hl" : "vodhl",
	"interview" : "vodinterview",
	'subject' : 'with',
	"summary" : "recap",
	"subjectlink" : "withlinks",
	'pbplink' : 'pbplinks',
	'colorlink' : 'colorlinks'
}

match_params = ['round', 'pbp', 'color', 'mvp', 'mvplink', 'hl', 'interview', 'subject', 'subjectlink','reddit',
				'pbplink', 'colorlink'
				]

def add_param(game, name, value):
	if name in param_lookup:
		name = param_lookup[name]
	game.add(name, value)
	
lmt = 0
for pagename in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % pagename)
	else:
		page = site.client.pages[pagename + '/Match Details']
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		
		all_data = []
		add_to_matches = []
		
		for template in wikitext.filter_templates():
			if template.name.matches('MatchDetails/Series'):
				game1 = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
				game2 = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
				game3 = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
				game4 = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
				game5 = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
				game_data = [game1, game2, game3, game4, game5]
				has_games = [False, False, False, False, False]
				series = []
				n_games = 0
				mh = False
				for param in template.params:
					name = str(param.name).strip()
					val = param.value.strip()
					if name == 'mh':
						mh = val
					if name.startswith('g1'):
						if val != '':
							has_games[0] = True
						add_param(game1, name[2:],val)
					elif name.startswith('g2'):
						if val != '':
							has_games[1] = True
						add_param(game2, name[2:], val)
					elif name.startswith('g3'):
						if val != '':
							has_games[2] = True
						add_param(game3, name[2:], val)
					elif name.startswith('g4'):
						if val != '':
							has_games[3] = True
						add_param(game4, name[2:], val)
					elif name.startswith('g5'):
						if val != '':
							has_games[4] = True
						add_param(game5, name[2:], val)
					elif name in match_params:
						series.append(param)
				for i in range(4,-1,-1):
					if not has_games[i]:
						del game_data[i]
					# we need to add the mh in for each game that exists if we're in the LPL lol rip
					elif mh:
						game_data[i].add('mh',mh)
				all_data.append(game_data)
				add_to_matches.append(series)
		
		data_page = site.client.pages['Data:' + pagename]
		data_text = data_page.text()
		data_wikitext = mwparserfromhell.parse(data_text)
		
		i = 0
		for template in data_wikitext.filter_templates():
			if template.name.matches('MatchSchedule'):
				if template.has('ff') and template.get('ff').value.strip() in ['1','2']:
					pass
				elif len(add_to_matches) > i:
					for param in add_to_matches[i]:
						name = str(param.name)
						if name in param_lookup:
							name = param_lookup[name]
						template.add(name, str(param.value))
					for j, game in enumerate(all_data[i]):
						template.add('game' + str(j+1),str(game))
					i = i + 1
		
		data_text_new = str(data_wikitext)
		if data_text_new != text:
			print('Saving page %s...' % data_page.name)
			data_page.save(data_text_new, summary = summary)
		else:
			print('Skipping page %s...' % data_page.name)
