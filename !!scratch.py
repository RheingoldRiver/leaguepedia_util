from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)
summary = 'Adding region to international tournaments by querying pages'

# page_list = site.cargo_client.page_list(
# 	tables="Tournaments",
# 	where="Region=\"International\"",
# 	fields="_pageName=Page",
# 	limit=5000
# )

title_list = [
	"International e-Culture Festival 2015",
	"International E-sports Festival 2019",
	"International Invitational Tournament 1",
	"International Invitational Tournament 2",
	"International Invitational Tournament 3",
	"International Invitational Tournament 4",
	"IPL LoLympics",
	"IPL Royale",
	"ISF 2019",
	"KCON 2014 Champions Festival",
	"Kung Fu Cup",
	"League of Legends International College Cup/2017 Season",
	"League of Legends International College Cup/2018 Season",
	"League of Legends International College Cup/2019 Season",
	"Legendary Gaming Easter Cup",
	"Legendary Gaming New Year's Cup",
	"Lone Star Clash 2",
	"Rampage King of The Hill Series",
	"Red Bull Player One 2019",
	"Reign of Gaming International Invitational",
	"Return of the Legends 2017",
	"Return of the Legends 2018",
	"Rift Rivals 2017",
	"Rift Rivals 2017/GPL-LJL-OPL",
	"Rift Rivals 2017/LCK-LPL-LMS",
	"Rift Rivals 2017/LCL-TCL",
	"Rift Rivals 2017/LLN-CLS-CBLOL",
	"Rift Rivals 2017/NA-EU",
	"Rift Rivals 2018",
	"Rift Rivals 2018/LCK-LPL-LMS",
	"Rift Rivals 2018/LCL-TCL-VCS",
	"Rift Rivals 2018/LLN-CLS-CBLOL",
	"Rift Rivals 2018/NA-EU",
	"Rift Rivals 2018/SEA-LJL-OPL",
	"Rift Rivals 2019",
	"Rift Rivals 2019/LCK-LPL-LMS-VCS",
	"Rift Rivals 2019/NA-EU",
	"Rift Rivals 2019/NA-EU/Showmatches",
	"Season 1 World Championship",
	"Season 2 World Championship",
	"Season 3 World Championship",
	"SL i-League LoL Invitational",
	"Sound Blaster Nations Championship",
	"Sweden vs. South Korea Friendly Match",
	"World e-Sports Masters 2012",
	"World GameMaster Tournament/2013",
	"Zona Esports - Movistar Riders Showmatch",
]

class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if not template.has('team'):
			return
		if template.has('region'):
			return
		team = template.get('team').value.strip()
		team_page = site.client.pages[team].resolve_redirect()
		team = team_page.name
		result = site.cargo_client.query(
			tables="Teams",
			where="_pageName=\"{}\"".format(
				site.cache.get('Team', team, 'link')
			),
			fields="Region"
		)
		if not result:
			return
		region = result[0]['Region']
		template.add('region', region, before='team')
		template.remove('team')
		template.add('team', team, before='region')


TemplateModifier(site, 'TeamRoster',
                 title_list=title_list,
                 tags="regions_in_intl_tournaments",
                 summary=summary).run()
