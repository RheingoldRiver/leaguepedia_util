from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'remove "Q for" from TRL qual2 param'  # Set summary

limit = -1
startat_page = 'Thailand Pro League/2018 Season/Spring Season'
this_template = site.pages['Template:TournamentResults/Line']  # Set template
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
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('TournamentResults/Line'):
				if template.has('qual2'):
					qual = template.get('qual2').value.strip()
					qual = qual.replace("'","").replace('Q for ','')
					template.add('qual2',qual)
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)