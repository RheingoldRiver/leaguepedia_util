from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Updating Standings args for consistency with new code'  # Set summary

limit = -1
startat_page = 'ECS/2016 Season/Summer Season'
this_template = site.pages['Template:StandingsStart']  # Set template
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
			if template.name.matches('StandingsStart'):
				i = 1
				s = str(i)
				places = []
				made_changes = False
				while template.has('bg' + s) or template.has('pl' + s):
					made_changes = True
					if template.has('bg' + s):
						template.add('row' + s, template.get('bg' + s).value.strip(), before = 'bg' + s)
						template.remove('bg' + s)
					if template.has('pl' + s):
						places.append(template.get('pl' + s).value.strip())
						template.remove('pl' + s)
					else:
						places.append('')
					i = i + 1
					s = str(i)
				if made_changes:
					if template.has('row1'):
						template.add('places', ','.join(places), before = 'row1')
					else:
						template.add('places', ','.join(places))
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)