from log_into_wiki import login
import mwparserfromhell
from clients import data_dragon_client
from helpers import wiki_helper

from pprint import pprint

# Login to the Wiki
site = login('bot','lol') # Set wiki

# Get pages for respective template
wiki = wiki_helper.WikiHelper()
pages = wiki.getPagesByTemplate(site, 'Template:Infobox Champion')

# Get all Champ data from DataDragon API
API_VERSION='latest'
client = data_dragon_client.DataDragonClient()
data = client.getChampionData(API_VERSION)
champ_list = data['data']

# Actual logic - This is straight up JANK
# Rito's api nests the name (we have as page title) inside an outer name which is different + we don't know
# Therefore we loop over every champ, checking inner name => O(n)^2 (i.e shit)

# For every champion page we have on the wiki
for page in pages:
	# Find the respective champion from the Rito DataDragon API results
	for champion in champ_list:
		isFound = False
		name = champ_list[champion]['name']
		if page.name == name:
			currentChampion = champ_list[champion]
			isFound = True
			break

	# If Champion was not found
	if isFound is False:
		print('champion not found!')
		raise Exception('Champion from page not found in Riot API. {} Not found.'.format(page.name))

	# Get the page text
	text = page.text()
	wikitext = mwparserfromhell.parse(text)

	for template in wikitext.filter_templates():
		if template.name.matches('Infobox Champion'):

			pprint(vars(template))
			print(template.get('be').value)
			
			# updateInfoBoxChampion(template)
	newtext = str(wikitext)

	# if text != newtext & page.name == 'Sona':
	# 	print('Saving page %s...' % page.name)
	# 	summary = 'Test Edit' # Set summary
	# 	page.save(newtext, summary=summary)
	# else:
	# 	print('Skipping page %s...' % page.name)

	break

