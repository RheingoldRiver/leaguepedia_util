from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lastepoch')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1 # set this to -1 to be unlimited
fieldname = 'OtherTag' # SET THIS TO PARAM


# startat_page = 'asdf'
this_template = site.pages['Template:Skills']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
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
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('Skills'):
				i = 1
				tbl = []
				changed = False
				while template.has(fieldname + str(i)):
					changed = True
					if template.get(fieldname + str(i)).value.strip() != '':
						tbl.append(template.get(fieldname + str(i)).value.strip())
					template.remove(fieldname + str(i))
					i += 1
				if changed:
					template.add(fieldname + 's', ', '.join(tbl))
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)