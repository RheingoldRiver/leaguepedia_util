from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
import json

titles = [
	"Data:Demacia Cup 2019",
	"Data:LDL Online Scrims League 2020/Spring Season",
	"Data:LDL/2019 Season/Spring Season/3",
	"Data:LDL/2019 Season/Spring Season/4",
	"Data:LDL/2019 Season/Spring Season/5",
	"Data:LDL/2019 Season/Spring Season/6",
	"Data:LDL/2019 Season/Spring Season/7",
	"Data:LDL/2019 Season/Spring Season/8",
	"Data:LDL/2019 Season/Spring Season/9",
	"Data:LDL/2019 Season/Summer Season/10",
	"Data:LDL/2019 Season/Summer Season/7",
	"Data:LDL/2020 Season/Spring Season/2",
	"Data:LDL/2020 Season/Summer Season/4",
	"Data:LDL/2020 Season/Summer Season/5",
	"Data:LPL Online Scrims League 2020/Spring Season"
]

with open('scoreboard_id_to_wanplus_url.json') as f:
	sb_to_wp_dict = json.load(f)
		
credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
summary = 'Automatically adding Wanplus URLs via SB intermediary, hopefully i did this right gl'

result = site.cargo_client.query(
	tables="ScoreboardGames=SG,Tournaments=T",
	join_on="SG.OverviewPage=T.OverviewPage",
	where="T.StandardLeague=\"LoL Development League\"",
	fields="SG.ScoreboardID_Wiki=ID,SG.MatchHistory=MH",
	limit="max",
)

qq_to_sb_dict = {}
for row in result:
	qq = row["MH"][-4:]
	if qq not in row:
		qq_to_sb_dict[qq] = [row["ID"]]
		continue
	qq_to_sb_dict[qq].append(row["ID"])
class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if not template.has('qq'):
			return
		qq = template.get('qq').value.strip()
		if qq not in qq_to_sb_dict:
			return
		for sb in qq_to_sb_dict[qq]:
			if sb in sb_to_wp_dict:
				template.add('wanplus', sb_to_wp_dict[sb], before='qq')
				return
			else:
				print('No entry for {}'.format(sb))
		print('Missing entry for {} on page {}'.format(qq, self.current_page.name))


TemplateModifier(site, 'MatchSchedule',
                 title_list=titles,
                 summary=summary).run()
