from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = "Removing unused teamhist params for players with automated news"


class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if not template.has('checkboxAutoTeams'):
			return
		if template.get('checkboxAutoTeams').value.strip() != 'Yes':
			return
		for i in range(1, 31):
			s = str(i)
			for param in ['teamhist', 'teamdate', 'teamrole']:
				param_name = '{}{}'.format(param, s)
				if template.has(param_name):
					template.remove(param_name)
		template.add('checkbox3', 'No')
		for param in ['team', 'team2']:
			if template.has(param):
				template.remove(param)
		for i in range(26, 31):
			if template.has('issub' + str(i)):
				template.remove('issub' + str(i))


TemplateModifier(site, 'Infobox Player',
                 # startat_page="PrZo",
                 summary=summary).run()