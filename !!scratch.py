from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)
summary = '"noteamhist" -> "low_content""'


class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if not template.has('noteamhist'):
			return
		noteamhist = template.get('noteamhist').value.strip()
		template.add('low_content', noteamhist, before = 'noteamhist')
		template.remove('noteamhist')


TemplateModifier(site, 'Infobox Player',
                 summary=summary).run()
