from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

year = '2019'
tournament = 'LPL 2019 Summer'
#########################################
# modify only above this line
#########################################
TEXT = """{{PlayerTabsHeader}}
{{PlayerYearStats}}"""

SUMMARY = "Autopopulating year player stats from tournament %s" % tournament

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Bot Edit'  # Set summary

overview_page = site.client.pages[tournament].redirects_to().name

pagelist = site.client.cargo_pagelist('Link', page_pattern="%s/Statistics/" + year,
	tables = 'ScoreboardPlayer',
	where = 'OverviewPage="%s"' % overview_page,
	fields = 'Link',
	group_by = 'Link',
	limit = 'max'
)

for page in pagelist:
	if not page.exists:
		print('Saving page %s...' % page.name)
		page.save(TEXT, summary=SUMMARY)
