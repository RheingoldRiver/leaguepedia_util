from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Add "game1" argument'  # Set summary

limit = -1
startat_page = 'LLN/2018 Season/Closing Season/Picks and Bans'
this_template = site.pages['Template:PicksAndBansS7']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
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
		print('Starting page %s...' % page.name)
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('PicksAndBansS7'):
				first = False
				if template.has('game1'):
					pass
				elif template.has('nocargo'):
					pass
				elif template.has('game'):
					if template.get('game').value.strip() == '1':
						first = True
				elif template.has('team1score') and template.has('team2score'):
					str1 = template.get('team1score').value.strip()
					str2 = template.get('team2score').value.strip()
					if str1 == 'FF' or str2 == 'FF':
						template.name = 'PicksAndBansForfeit'
					elif str1 != '' and str2 != '':
						s1 = int(str1)
						s2 = int(str2)
						if s1 + s2 == 1:
							first = True
				if first:
					template.add('game1','Yes')
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)