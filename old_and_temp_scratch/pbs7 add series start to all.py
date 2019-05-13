from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Add "game1" argument'  # Set summary

limit = -1
startat_page = 'LLN/2018 Season/Closing Season/Picks and Bans'
this_template = site.pages['Template:PicksAndBansS7']  # Set template

pages = [site.pages['LCS/2019 Season/Spring Season/Picks and Bans/4-6']]

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	if lmt < -1:
		print("Skipping page %s" % page.name)
	else:
		print('Starting page %s...' % page.name)
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('PicksAndBansS7'):
				template.add('game1', 'Yes')
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)