from river_mwclient.esports_site import EsportsSite

year = '2019'
tournament = 'LPL 2019 Summer'
#########################################
# modify only above this line
#########################################
TEXT = """{{PlayerTabsHeader}}
{{PlayerYearStats}}"""

SUMMARY = "Autopopulating year player stats from tournament %s" % tournament

site = EsportsSite('lol', user_file="me") # Set wiki
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
