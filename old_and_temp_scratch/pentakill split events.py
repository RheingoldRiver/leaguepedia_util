from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Separating event link to |eventlink='  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:PentakillLine']  # Set template
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
			if template.name.matches('PentakillLine'):
				val = template.get(3).value.strip(' []')
				if '|' in val or '{{!}}' in val:
					if '|' in val:
						val_tbl = val.split('|')
					elif '{{!}}' in val:
						val_tbl = val.split('{{!}}')
					template.add('eventlink', val_tbl[0], before=4)
					template.add(3, val_tbl[1])
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)