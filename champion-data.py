from log_into_wiki import login
import mwparserfromhell
from clients import data_dragon_client
from helpers import wiki_helper
from mappers import champion_data_mapper

from pprint import pprint

def updateTemplate(template, currentChampion):
	# We don't care about crit or crit scaling
	del currentChampion['stats']['crit']
	del currentChampion['stats']['critperlevel']
	# Stats 
	for stat, value in currentChampion['stats'].items():
		template.add(champion_data_mapper.datamapper['stats'][stat], str(value))

	# Tags ()
	template.add(champion_data_mapper.datamapper['tags'][0], currentChampion['tags'][0])
	if len(currentChampion['tags']) == 2:
		template.add(champion_data_mapper.datamapper['tags'][1], currentChampion['tags'][1])

	# Title
	template.add(champion_data_mapper.datamapper['title'], currentChampion['title'])

	# Partype (Resource)
	template.add(champion_data_mapper.datamapper['partype'], currentChampion['partype'])

def main():
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
	# 'Better' solution (more efficient but kinda more clutter) is to use hidden variables 
	# In the infobox

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
			print('How did you get here?')
			raise Exception('Champion from page not found in Riot API. {} Not found.'.format(page.name))

		# Get the page text
		text = page.text()
		wikitext = mwparserfromhell.parse(text)

		for template in wikitext.filter_templates():
			if template.name.matches('Infobox Champion'):
				updateTemplate(template, currentChampion)
				
		newtext = str(wikitext)
		
		if text != newtext:
			with open('1-output.txt', 'a') as the_file:
				the_file.write(text)

			with open('2-output.txt', 'a') as the_file_2:
				the_file_2.write(newtext)

			# print('Saving page %s...' % page.name)
		# 	summary = 'Test Edit' # Set summary
		# 	page.save(newtext, summary=summary)
		# else:
		# 	print('Skipping page %s...' % page.name)

main()
