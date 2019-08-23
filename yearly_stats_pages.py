import log_into_wiki
from extended_page import ExtendedPage

site = log_into_wiki.login('bot', 'lol')

create_text = """{{PlayerTabsHeader}}
{{PlayerYearStats}}"""

overview_create_text = """{{PlayerTabsHeader}}
{{CareerPlayerStats}}"""

redirect_text = '#redirect[[%s]]'

summary= "Automatically discovering & creating year player stats"

results = site.cargoquery(
	tables='ScoreboardPlayer=SP,_pageData=PD1,_pageData=PD2',
	join_on='SP.Link=PD1._pageName,SP.StatsPage=PD2._pageName',
	where='PD1._pageName IS NOT NULL and PD2._pageName IS NULL and BINARY PD1._pageName=BINARY SP.Link',
	fields="SP.StatsPage=StatsPage, PD1._isRedirect=IsRedirect",
	group_by= "SP.StatsPage",
	limit='max'
)

def save_pages(page):
	page.save(create_text, summary=summary)
	base_stats_page = site.pages[page.base_title + '/Statistics']
	if not base_stats_page.exists:
		base_stats_page.save(overview_create_text, summary=summary)

for result in results:
	stats_page = ExtendedPage(site.pages[result['StatsPage']])
	if result['IsRedirect'] == '0':
		save_pages(stats_page)
		continue
	target = site.pages[stats_page.base_title].redirects_to()
	target_stats_page_name = stats_page.name.replace(stats_page.base_title, target.name)
	target_stats_page = ExtendedPage(site.pages[target_stats_page_name])
	save_pages(target_stats_page)
	stats_page.save(redirect_text % target_stats_page.name)
