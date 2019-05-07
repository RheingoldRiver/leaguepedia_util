from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
startat_player = 'Underdogs Season 3'
this_template = site.pages['Template:Infobox Tournament']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_player)
except NameError as e:
	startat = -1
print(startat)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		pb_page = site.pages[page.name + '/Picks and Bans']
		if pb_page.text() == '':
			print("Skipping page %s" % page.name)
		else:
			text = pb_page.text()
			wikitext = mwparserfromhell.parse(text)
			makePBH = False
			for template in wikitext.filter_templates():
				if template.name.matches('PicksAndBansS7'):
					makePBH = True
					break
			if makePBH:
				text = page.text()
				wikitext = mwparserfromhell.parse(text)
				tabs = ''
				for template in wikitext.filter_templates():
					if 'Tabs' in template.name:
						tabs = template.name.strip()
						break
				newtext = '{{' + tabs + '}}\n{{PBHistoryTournament}}'
				print('Saving page %s...' % page.name)
				newpage = site.pages[page.name + '/Pick-Ban History']
				newpage.save(newtext, summary = summary)
			else:
				print('Skipping page %s bc no PBS7' % page.name)