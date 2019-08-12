from log_into_wiki import *

year = '2019'
tournament = 'LDL 2019 Summer'
#########################################
# modify only above this line
#########################################
TEXT = """{{PlayerTabsHeader}}
{{PlayerYearStats}}"""

SUMMARY = "Autopopulating year player states from tournament %s" % tournament

site = login('me', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

overview_page = site.pages[tournament].redirects_to().name

pagelist = site.cargo_pagelist('Link', page_pattern="%s/Statistics/" + year,
							   tables = 'ScoreboardPlayer',
							   where = 'OverviewPage="%s"' % overview_page,
							   fields = 'Link',
							   limit = 'max'
							   )
for page in pagelist:
	if not page.exists:
		print('Saving page %s...' % page.name)
		page.save(TEXT, summary=SUMMARY)
