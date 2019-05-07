from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'update to new params'  # Set summary

limit = -1
startat_page = 'ESL Balkans League/Season V'
this_template = site.pages['Template:GameSchedule5']  # Set template
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
			if template.name.matches('GameSchedule5'):
				if template.has('t1score'):
					template.get('t1score').name = 'team1score'
				if template.has('t2score'):
					template.get('t2score').name = 'team2score'
				if template.has('post-match'):
					template.get('post-match').name = 'reddit'
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)