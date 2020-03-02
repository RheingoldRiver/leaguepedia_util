from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'Graves/Skins'
this_template = site.client.pages['Template:ChampionSkinsLine']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

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
	print(page.name)
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates(recursive=False):
		if template.name.matches(['ChampionSkinsLine']):
			if not template.has('chroma'):
				continue
			chroma = mwparserfromhell.parse(template.get('chroma').value.strip())
			for tl in chroma.filter_templates():
				if tl.name.matches('ChromaBox'):
					if tl.has('rp'):
						template.add('chroma_rp', tl.get('rp').value.strip())
					template.add('chroma_date', tl.get('releasedate').value.strip())
					if tl.has('special'):
						template.add('chroma_special', tl.get('special').value.strip())
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
