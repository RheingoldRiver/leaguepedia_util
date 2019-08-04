from log_into_wiki import *
import re

site = login('me','zelda') # Set wiki
summary = 'Rename Modules' # Set summary

limit = 10
#startat_page = 'asdf'
lmt = 0
for p in site.allpages(namespace=828):
	if limit == lmt:
		break
	lmt += 1
	print(p.name)
	text = p.text()
	text_table = text.split('\n')
	newlines = []
	for line in text_table:
		newlines.append(re.sub(r"require\( *[\'\"]Module:Utils(.+?)['\"] *\)", r"require('Module:\1Util')",line))
	newtext = '\n'.join(newlines)
	if text != newtext:
		p.save(newtext)