from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:Timeline']  # Set template
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
			if template.name.matches('AutoTimeline') or template.name.matches('Timeline'):
				i = 1
				s = str(i)
				places = []
				added = False
				while template.has('p' + s + 'color'):
					added = True
					places.append(template.get('p' + s + 'color').value.strip())
					template.remove('p' + s + 'color')
					i = i + 1
					s = str(i)
				if added:
					template.add('places', ', '.join(places))
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)