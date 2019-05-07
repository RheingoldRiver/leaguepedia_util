from log_into_wiki import *
limit = -1
#startat_page = 'Donut'
template = 'Infobox Player'
form = 'Infobox Player'

site = login('bot','lol')

########################################

result = site.api('query', format='json',
				  list='embeddedin',
				  eititle='Template:' + template,
				  einamespace = '0',
				  eilimit = 'max'
				  )

pages = []

for p in result['query']['embeddedin']:
	pages.append(p['title'])

try:
	startat = pages.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
failures = []

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	print(page)
	if lmt <= startat:
		pass
	else:
		try:
			site.api('pfautoedit', format='json',
					 form = form,
					 target = page
					 )
		except Exception as e:
			failures.append(page + "(" + e.args[0] + ")")

print('Done! Printing failures...')

for failure in failures:
	print(failure)