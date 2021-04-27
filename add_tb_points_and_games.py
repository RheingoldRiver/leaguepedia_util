from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials
import mwparserfromhell

credentials = AuthCredentials(user_file="me")
site = EsportsClient('rl-esports', credentials=credentials)  # Set wiki
summary = 'Fixing Formatting from GS5 to MS'  # Set summary
limit = -1
startat = -1

#################################
# Ignore everything above here
#################################

#pagename = 'LPL/2019 Season/Spring Season'
pointstype = 'none' # none, bo3points, bo2, bo3pointsopl

remove_params = ['round','start','end','hide', 'nosemantics']
rename_params = {
	't1score': 'team1score',
	't2score': 'team2score',
}
tb_names = ['tb', 'tiebreakers', 'tiebreaker']
gameschedule_template_name = 'GameSchedule5'

max_scores = {
	'bo3points' : 3,
	'bo3pointsopl' : 3,
	'none' : 1,
	'bo2' : 2
}

if pointstype not in max_scores:
	raise IndexError

# pages_var = [site.client.pages['Data:' + pagename]]

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages_var = [site.client.pages['Data:' + page.strip()] for page in pages]

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
		continue
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	template: mwparserfromhell.nodes.Template
	for template in wikitext.filter_templates():
		if not template.name.matches(gameschedule_template_name) and not template.name.matches('MatchSchedule'):
			continue
		for name in rename_params.keys():
			if template.has(name):
				param = template.get(name)
				param.name = rename_params[name]
		template.name = 'MatchSchedule'
		score1 = 0
		score2 = 0
		if template.has('team1score') and template.has('team2score'):
			if template.get('team1score').value.strip() != '' and template.get('team2score').value.strip() != '':
				str1 = template.get('team1score').value.strip()
				str2 = template.get('team2score').value.strip()
				score1 = 0
				score2 = 0
				if str1 == 'FF':
					template.add('ff', '1')
					score2 = max_scores[pointstype]
				elif str2 == 'FF':
					template.add('ff','2')
					score1 = max_scores[pointstype]
				else:
					score1 = int(str1)
					score2 = int(str2)
				if pointstype == 'bo3points':
					template.add('team1pointstb', str(score1 - score2), before='date')
					template.add('team2pointstb', str(score2 - score1), before='date')
				elif pointstype == 'bo3pointsopl':
					points1 = score1 + (1 if score2 == 0 else 0)
					points2 = score2 + (1 if score1 == 0 else 0)
					template.add('team1points', str(points1), before='date')
					template.add('team2points', str(points2), before='date')
				elif pointstype == 'bo2':
					points1 = 3 if score1 == 2 else score1
					points2 = 3 if score2 == 2 else score2
					template.add('team1points', str(points1), before='date')
					template.add('team2points', str(points2), before='date')
		if template.has('round'):
			if template.get('round').value.strip().lower() in tb_names:
				template.add('istb','yes', before = 'round')
		for param in remove_params:
			if template.has(param):
				template.remove(param)
		for i in range(0, score1 + score2):
			s = str(i + 1)
			game = mwparserfromhell.nodes.template.Template('MatchSchedule/Game')
			thisvod = 'vod' + s
			if template.has(thisvod):
				game.add('vod', str(template.get(thisvod).value.strip()))
				template.remove(thisvod)
			if not template.has('game' + s):
				template.add('game' + s, str(game))
		if template.has('winner') and template.get('winner').value.strip().lower() == 'draw':
			template.add('winner','0')
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
