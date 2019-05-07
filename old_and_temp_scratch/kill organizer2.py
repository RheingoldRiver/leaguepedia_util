from log_into_wiki import *
import mwparserfromhell, re

site = login('bot', 'pubg-esports')  # Set wiki
summary = 'redo otherwikis to match infobox player'  # Set summary

limit = -1
startat_page = 'Team Vidar'
this_template = site.pages['Template:Infobox Team']  # Set template
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
	if lmt < startat or page.namespace != 0:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('Infobox Team') or template.name.matches('Infobox_Team'):
				i = 1
				otherwikis = []
				while template.has('title' + str(i)):
					val = template.get('title' + str(i)).value.strip()
					val = re.sub(r'<!--.*-->','',val)
					if val != '':
						otherwikis.append(val)
					template.remove('title' + str(i))
					i += 1
				if not template.has('otherwikis'):
					template.add('otherwikis', ','.join(otherwikis))
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)