from log_into_wiki import login
from extended_page import ExtendedPage

CREATE_TEXT = """{{{{{}TabsHeader}}}}
{{{{{}YearStats}}}}"""

OVERVIEW_CREATE_TEXT = """{{{{{}TabsHeader}}}}
{{{{Career{}Stats}}}}"""

MH_CREATE_TEXT = """{{{{{}TabsHeader}}}}
{{{{MatchHistory{}}}}}"""

class StatsCreator(object):
	def __init__(self, page_type):
		self.site = login('bot', 'lol')
		self.summary = "Automatically discovering & creating year player & team stats"
		self.error_page = self.site.pages['Log:Failed Yearly Stats Pages']
		self.errors = set()
		self.create_text = CREATE_TEXT.format(page_type, page_type)
		self.overview_create_text = OVERVIEW_CREATE_TEXT.format(page_type, page_type)
		self.mh_create_text = MH_CREATE_TEXT.format(page_type, page_type)
		self.redirect_text = '#redirect[[%s]]'
	
	def run(self):
		results = self.get_page_list()
		for result in results:
			if result['StatsPage'].endswith('Statistics'):
				self.report_error(result['OverviewPage'])
				continue
			stats_page = ExtendedPage(self.site.pages[result['StatsPage']])
			if result['IsRedirect'] == '0':
				self.save_pages(stats_page)
				continue
			target = self.site.pages[stats_page.base_title].redirects_to()
			target_stats_page_name = stats_page.name.replace(stats_page.base_title, target.name)
			target_stats_page = ExtendedPage(self.site.pages[target_stats_page_name])
			self.save_pages(target_stats_page)
			stats_page.save(self.redirect_text % target_stats_page.name)
		self.log_all_errors()
	
	def get_page_list(self):
		# pass, but we don't want it giving a warning in self.run()
		return []
	
	def save_pages(self, page: ExtendedPage):
		base_title = page.base_title
		self.save_stats_year(page)
		self.save_stats_overview(self.site.pages[base_title + '/Statistics'])
		self.save_mh(self.site.pages[base_title + '/Match History'])
	
	def save_stats_overview(self, page):
		if not page.exists:
			page.save(self.overview_create_text, summary=self.summary)
	
	def save_mh(self, page):
		if not page.exists:
			page.save(self.mh_create_text, summary=self.summary)
	
	def save_stats_year(self, page):
		page.save(self.create_text, summary=self.summary)
	
	def report_error(self, title):
		self.errors.add(title)
	
	def log_all_errors(self):
		if not self.errors:
			return
		self.error_page.append('\n' + '\n'.join(['[[%s]]' % _ for _ in list(self.errors)]), summary=self.summary)
	

class TeamStatsCreator(StatsCreator):
	def __init__(self):
		super().__init__('Team')
	
	def get_page_list(self):
		results = self.site.cargoquery(
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
		results = self.site.cargoquery(
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
