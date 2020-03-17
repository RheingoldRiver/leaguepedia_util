import mwparserfromhell
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

summary = 'Semi-automatically migrating MD pages to Data namespace (Python)'
pagename = 'OPL/2018 Season/Split 1'
credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
limit = -1
startat = -1

pages_var = [ pagename ]

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()
# pages_var = [page.strip() for page in pages]

param_lookup = {
	'pb' : 'vodpb',
	'game' : 'vodstart',
	'post' : 'vodpost',
	'hl' : 'vodhl',
	'int' : 'vodinterview'
}

param_list = [ 'pb', 'game', 'post', 'int', 'hl' ]


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
		page = site.client.pages[pagename + '/VODs']
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		
		all_data = []
		
		for template in wikitext.filter_templates():
			if template.name.matches('VODLine'):
				new_params = []
				for param in template.params:
					if param.name.strip() in param_list:
						new_params.append(param)
				all_data.append(new_params)
		data_page = site.client.pages['Data:' + pagename]
		data_text = data_page.text()
		data_wikitext = mwparserfromhell.parse(data_text)
		
		i = 0
		for template in data_wikitext.filter_templates(recursive = False):
			j = 1
			s = str(j)
			if template.name.matches('MatchSchedule'):
				try:
					while template.has('game' + s):
						sub_template_wikicode = mwparserfromhell.parse(template.get('game' + s).value.strip())
						sub_template = sub_template_wikicode.filter_templates()[0]
						for param in all_data[i]:
							add_param(sub_template, param.name.strip(), param.value.strip())
						template.add('game' + s, str(sub_template_wikicode))
						j = j + 1
						s = str(j)
						i = i + 1
				except IndexError as e:
					print(str(i))
					break
		
		data_text_new = str(data_wikitext)
		if data_text_new != text:
			print('Saving page %s...' % data_page.name)
			data_page.save(data_text_new, summary=summary)
		else:
			print('Skipping page %s...' % data_page.name)
