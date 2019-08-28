from log_into_wiki import *

site = login('me','lol') # Set wiki
summary = 'Automatically creating tournament StandardName redirect'

response = site.api('cargoquery', tables="Tournaments,_pageData",
					join_on = 'Tournaments.StandardName_Redirect=_pageData._pageName',
					where='_pageData._pageName IS NULL AND Tournaments.StandardName_Redirect IS NOT NULL',
					fields='Tournaments.StandardName_Redirect=Name,Tournaments._pageName=Target',
					limit='max'
					)

for item in response['cargoquery']:
	data = item['title']
	name = data['Name']
	target = data['Target']
	text = '#redirect[[%s]]' % target
	site.pages[name].save(text)
