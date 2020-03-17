from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from extended_page import ExtendedPage

YEAR_CREATE_TEXT = """{{{{{}TabsHeader}}}}
{{{{{}YearStats}}}}"""

OVERVIEW_CREATE_TEXT = """{{{{{}TabsHeader}}}}
{{{{Career{}Stats}}}}"""

MH_CREATE_TEXT = """{{{{{}TabsHeader}}}}
{{{{MatchHistory{}}}}}"""

class StatsCreator(object):
	def __init__(self, page_type):
		self.credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
		self.summary = "Automatically discovering & creating year player & team stats"
		self.error_page = 'Failed Yearly Stats Pages'
		self.create_text = YEAR_CREATE_TEXT.format(page_type, page_type)
		self.overview_create_text = OVERVIEW_CREATE_TEXT.format(page_type, page_type)
		self.mh_create_text = MH_CREATE_TEXT.format(page_type, page_type)
		self.redirect_text = '#redirect[[%s]]'
	
	def run(self):
		results = self.get_page_list()
		for result in results:
			if result['StatsPage'].endswith('Statistics'):
				self.site.log_error_content(title=result['OverviewPage'])
				continue
			stats_page = ExtendedPage(self.site.client.pages[result['StatsPage']])
			if result['IsRedirect'] == '0':
				self.save_pages(stats_page)
				continue
			target = self.site.client.pages[stats_page.base_title].redirects_to()
			target_stats_page_name = stats_page.name.replace(stats_page.base_title, target.name)
			target_stats_page = ExtendedPage(self.site.client.pages[target_stats_page_name])
			self.save_pages(target_stats_page)
			stats_page.save(self.redirect_text % target_stats_page.name)
		self.site.client.report_all_errors(self.error_page)
	
	def get_page_list(self):
		# pass, but we don't want it giving a warning in self.run()
		return []
	
	def save_pages(self, page: ExtendedPage):
		base_title = page.base_title
		self.save_stats_year(page)
		self.save_stats_overview(self.site.client.pages[base_title + '/Statistics'])
		self.save_mh(self.site.client.pages[base_title + '/Match History'])
	
	def save_stats_overview(self, page):
		if not page.exists:
			page.save(self.overview_create_text, summary=self.summary)
	
	def save_mh(self, page):
		if not page.exists:
			page.save(self.mh_create_text, summary=self.summary)
	
	def save_stats_year(self, page):
		page.save(self.create_text, summary=self.summary)
	

class TeamStatsCreator(StatsCreator):
	def __init__(self):
		super().__init__('Team')
	
	def get_page_list(self):
		results = self.site.cargo_client.query(
			tables='ScoreboardTeam=ST,_pageData=PD1,_pageData=PD2',
			join_on='ST.Team=PD1._pageName,ST.StatsPage=PD2._pageName',
			where='PD1._pageName IS NOT NULL and PD2._pageName IS NULL and BINARY PD1._pageName=BINARY ST.Team',
			fields="ST.StatsPage=StatsPage, PD1._isRedirect=IsRedirect,ST.OverviewPage=OverviewPage",
			group_by="ST.StatsPage",
			limit='max'
		)
		return results
	
	def save_stats_overview(self, page):
		pass

class PlayerStatsCreator(StatsCreator):
	def __init__(self):
		super().__init__('Player')
	
	def get_page_list(self):
		results = self.site.cargo_client.query(
			tables='ScoreboardPlayer=SP,_pageData=PD1,_pageData=PD2',
			join_on='SP.Link=PD1._pageName,SP.StatsPage=PD2._pageName',
			where='PD1._pageName IS NOT NULL and PD2._pageName IS NULL and BINARY PD1._pageName=BINARY SP.Link',
			fields="SP.StatsPage=StatsPage, PD1._isRedirect=IsRedirect,SP.OverviewPage=OverviewPage",
			group_by="SP.StatsPage",
			limit='max'
		)
		return results

if __name__ == '__main__':
	PlayerStatsCreator().run()
	TeamStatsCreator().run()
