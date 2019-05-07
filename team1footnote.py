from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'team1footnote'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:MatchSchedule']  # Set template
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
			if template.name.matches('MatchSchedule'):
				if template.has('footnote1'):
					f = template.get('footnote1').value.strip()
					template.add('team1footnote', f, before = 'footnote1')
					template.remove('footnote1')
				if template.has('footnote2'):
					f = template.get('footnote2').value.strip()
					template.add('team2footnote', f, before = 'footnote2')
					template.remove('footnote2')
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)