from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Updating player concepts to use uc-first links only'  # Set summary

limit = -1
startat_page = 'Concept:Carbono/Games'
this_template = site.pages['Template:PlayerGamesConcept']  # Set template
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
		names = []
		for template in wikitext.filter_templates():
			if template.name.matches('PlayerGamesConcept'):
				i = 1
				while template.has(i):
					s = template.get(i).value.strip()
					name = s[0].upper() + s[1:]
					if name in names:
						pass
					else:
						names.append(name)
					i +=1
				
		output = '|'.join(names)
		newtext = '{{PlayerGamesConcept|' + output + '}}'
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)