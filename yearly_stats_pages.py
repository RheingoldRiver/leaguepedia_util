from extended_site import GamepediaSite
from extended_page import ExtendedPage
import mwclient

site = GamepediaSite('me', 'lol')

create_text = """{{PlayerTabsHeader}}
{{PlayerYearStats}}"""

overview_create_text = """{{PlayerTabsHeader}}
{{CareerPlayerStats}}"""

mh_create_text = """{{PlayerTabsHeader}}
{{MatchHistoryPlayer}}"""

redirect_text = '#redirect[[%s]]'

summary= "Automatically discovering & creating year player stats"

error_page = site.pages['Maintenance:Failed Yearly Stats Pages']
errors = set()

results = site.cargoquery(
	tables='ScoreboardPlayer=SP,_pageData=PD1,_pageData=PD2',
	join_on='SP.Link=PD1._pageName,SP.StatsPage=PD2._pageName',
	where='PD1._pageName IS NOT NULL and PD2._pageName IS NULL and BINARY PD1._pageName=BINARY SP.Link',
	fields="SP.StatsPage=StatsPage, PD1._isRedirect=IsRedirect,SP.OverviewPage=OverviewPage",
	group_by= "SP.StatsPage",
	limit='max'
)

def save_pages(page):
	page.save(create_text, summary=summary)
	base_stats_page = site.pages[page.base_title + '/Statistics']
	if not base_stats_page.exists:
		base_stats_page.save(overview_create_text, summary=summary)
	mh_page = site.pages[page.base_title + '/Match History']
	if not mh_page.exists:
		mh_page.save(mh_create_text, summary=summary)

for result in results:
	if result['StatsPage'].endswith('Statistics'):
		errors.add(result['OverviewPage'])
		continue
	stats_page = ExtendedPage(site.pages[result['StatsPage']])
	if result['IsRedirect'] == '0':
		save_pages(stats_page)
		continue
	target = site.pages[stats_page.base_title].redirects_to()
	target_stats_page_name = stats_page.name.replace(stats_page.base_title, target.name)
	target_stats_page = ExtendedPage(site.pages[target_stats_page_name])
	save_pages(target_stats_page)
	stats_page.save(redirect_text % target_stats_page.name)

if errors:
	error_page.save(error_page.text() + '\n' + '\n'.join(['[[%s]]' % _ for _ in list(errors)]), summary=summary)
