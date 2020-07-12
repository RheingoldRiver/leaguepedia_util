from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
summary = '+ wp display in MatchDetails'

titles = [
          "Demacia Cup/2018 Winter",
          "LDL Online Scrims League 2020/Spring Season",
          "LDL/2018 Season/Grand Finals",
          "LDL/2019 Season/Spring Playoffs",
          "LDL/2019 Season/Spring Season",
          "LDL/2019 Season/Summer Playoffs",
          "LDL/2019 Season/Summer Season",
          "LDL/2020 Season/Spring Season",
          "LDL/2020 Season/Summer Season",
          "LPL Online Scrims League 2020/Spring Season",
          "LPL/2018 Season/Regional Finals",
          "LPL/2018 Season/Spring Playoffs",
          "LPL/2018 Season/Spring Season",
          "LPL/2018 Season/Summer Playoffs",
          "LPL/2018 Season/Summer Season",
          "LPL/2019 Season/Regional Finals",
          "LPL/2019 Season/Spring Playoffs",
          "LPL/2019 Season/Spring Season",
          "LPL/2019 Season/Summer Playoffs",
          "LPL/2019 Season/Summer Season",
          "LPL/2020 Season/Spring Playoffs",
          "LPL/2020 Season/Spring Season",
          "Rift Rivals 2018/LCK-LPL-LMS"]

class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if not template.has('matchfields'):
			template.add('matchfields', 'wp')
			return
		matchfields = template.get('matchfields').value.strip()
		template.add(matchfields, matchfields + ',wp')


TemplateModifier(site, 'MatchDetails',
                 title_list=titles,
                 summary=summary).run()
