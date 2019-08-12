from log_into_wiki import *

site = login('wow', 'me')

response = site.api('cargoquery',
					fields = '_pageName=Page,_categories=Categories'
					# TODO
					)

for result in response['cargoquery']:
	cat = result['title']['Page']
	for page in site.categories[cat.replace('Category:','')]:
		text = page.text()
		# TODO
		page.save(text)
	cat_page = site.pages[cat]
	cat_page.move(new_name_here)
