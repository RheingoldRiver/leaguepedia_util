from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Use just |player=, no |link='  # Set summary


class TemplateModifier(TemplateModifierBase):
	def update_template(self):
		if not self.current_template.has('link'):
			return
		player = self.current_template.get('player').value.strip()
		link = self.current_template.get('link').value.strip()
		if not link.lower().startswith(player.lower()):
			return
		self.current_template.remove('link')
		self.current_template.add('player', link)


TemplateModifier(site, 'TeamRoster/Line',
                 startat_page="Prime League 2nd Division/2020 Season/Spring Season",
				 summary=summary).run()