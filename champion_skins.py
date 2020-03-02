from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'Hecarim'
this_template = site.client.pages['Template:Infobox Champion']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

params = ['name', 'rp', 'date', 'chroma', 'special', 'legacy']

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	skins = []
	for template in wikitext.filter_templates():
		if template.name.matches(['Infobox Champion']):
			i = 1
			while template.has('skin' + str(i) + 'name'):
				skin = mwparserfromhell.nodes.Template('ChampionSkinsLine')
				for param in params:
					if template.has('skin' + str(i) + param):
						skin.add(param, template.get('skin' + str(i) + param).value.strip())
				skins.append(str(skin))
				i += 1
	new_page = site.client.pages[page.name + '/Skins']
	new_page.save('{{ChampionTabsHeader}}\n{{ChampionSkinsStart}}\n' + '\n'.join(skins) + '\n{{ChampionSkinsEnd}}')
