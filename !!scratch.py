from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
import csv

with open('qq to wp.csv', mode='r') as infile:
	reader = csv.reader(infile)
	qq_dict = {rows[0]:rows[1] for rows in reader}
		
credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)
summary = 'Automatically adding Wanplus URLs'


class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if not template.has('qq'):
			return
		qq = template.get('qq').value.strip()
		if qq not in qq_dict:
			print('Missing entry for {} on page {}'.format(qq, self.current_page.name))
			return
		template.add('wanplus', qq_dict[qq], before='qq')


TemplateModifier(site, 'MatchSchedule',
                 quiet=True,
                 startat_page="Data:Rift Rivals 2018/LCK-LPL-LMS",
                 summary=summary).run()
