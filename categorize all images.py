from log_into_wiki import *
import mwparserfromhell

site = login('bot','battleriteroyale') # Set wiki
summary = 'Adding default license' # Set summary

limit = -1
pages = site.allpages(namespace = '6')

lmt = 0
for page in pages:
	print(page.name)
	if lmt == limit:
		break
	lmt += 1
	if lmt < 400:
		print("Skipping page %s" % page.name)
		continue
	text = page.text()
	newtext = ''
	if text == '':
		newtext = '== License ==\n{{Copyright Stunlock Studios}}'
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)