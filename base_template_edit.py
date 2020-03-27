from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
from river_mwclient.page_modifier import PageModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Clean up bundle/loot exclusive to their own args'  # Set summary


class PageModifier(PageModifierBase):
	def update_plaintext(self):
		return
	
	def update_wikitext(self):
		return


class TemplateModifier(TemplateModifierBase):
	def update_template(self):
		return


TemplateModifier(site, 'TEMPLATEYOUCAREABOUT',
				 summary=summary).run()
