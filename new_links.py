from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell, re

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials) #  set wiki
summary = 'Changing links/display to be just 1 field, with link only'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'Challengers Korea/2017 Season/Spring Season/Scoreboards/Week 3'
this_template = site.client.pages['Module:Scoreboard']  # Set template
pages = this_template.embeddedin()

#pages = [site.pages['Data:Challengers Korea/2019 Season/Spring Season']]

def links_to_display(template):
	if not template.has('name'):
		return
	name = template.get('name').value.strip()
	if '{{!}}' in name:
		template.add('name', name.split('{{!}}')[0])
	name = template.get('name').value.strip()
	if not template.has('link'):
		template.add('link', name, before='name')
		template.remove('name')
		return
	display_str = template.get('name').value.strip()
	link_str = template.get('link').value.strip()
	displays = display_str.split(',')
	links = link_str.split(',')
	new = []
	for i, v in enumerate(displays):
		if i < len(links) and links[i] != '':
			uc_display = v[0].upper() + v[1:]
			regex = r'^' + re.escape(uc_display)
			link = re.sub(regex, v, links[i])
			new.append(link)
			continue
		new.append(v)
	template.add('link', ','.join(new))
	template.remove('name')

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
	for template in wikitext.filter_templates():
		if template.name.matches(['MatchRecapS8/Player']):
			links_to_display(template)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)