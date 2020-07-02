from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.page_modifier import PageModifierBase
from river_mwclient.wiki_time_parser import time_from_template


class PageModifier(PageModifierBase):
	def update_wikitext(self, wikitext):
		for template in wikitext.filter_templates():
			if not template.name.matches(['MatchRecapS8', 'Scoreboard/Season 3', 'Scoreboard/Season 4', 'Scoreboard/Season 5', 'Scoreboard/Season 5', 'Scoreboard/Season 6', 'Scoreboard/Season 7', 'Scoreboard/Season 8']):
				continue
			date_time = time_from_template(template)
			if date_time is not None:
				template.add('dst', date_time.dst)

if __name__ == '__main__':
	credentials = AuthCredentials(user_file='bot')
	site = EsportsClient('lol', credentials=credentials)  # Set wiki
	PageModifier(site, page_list=site.pages_using('Scoreboard/Button'), summary="Fix dst").run()