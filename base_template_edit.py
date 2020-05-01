from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.page_modifier import PageModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Bot edit'  # Set summary


class PageModifier(PageModifierBase):
	def update_plaintext(self):
		return
	
	def update_wikitext(self):
		return


PageModifier(site,
				 summary=summary).run()
