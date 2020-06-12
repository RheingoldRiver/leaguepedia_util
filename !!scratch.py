from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)
summary = 'guess local timezone'

leagues = {
	"2015 All-Star Event": "PST",
	"2015 International Wildcard Invitational": "CET",
	"2015 International Wildcard Tournament": "CET",
	"2016 International Wildcard Qualifier": "CET",
	"All-Star": "International",
	"Battle of the Atlantic": "International",
	"BGS": "CET",
	"Brasil Mega Arena": "CET",
	"Brazil Mega Cup": "CET",
	"Brazilian Championship Series": "CET",
	"Brazilian Challenger Circuit": "CET",
	"Challengers Korea": "KST",
	"Circuit Brazilian League of Legends": "CET",
	"Circuito de Leyendas Norte": "PST",
	"Circuito de Leyendas Sur": "PST",
	"CIS Challenger League": "CET",
	"Copa Latinoamérica Sur": "PST",
	"Demacia Cup": "KST",
	"DreamHack": "CET",
	"Elite Challenger Series": "KST",
	"ESL Brasil Premier League": "CET",
	"Europe League Championship Series": "CET",
	"Europe Challenger Series": "CET",
	"European Masters": "CET",
	"Garena Premier League": "KST",
	"IGN Pro League": "PST",
	"Intel Extreme Masters": "International",
	"KeSPA": "KST",
	"League of Legends Championship Series": "PST",
	"League of Legends Nova League": "KST",
	"League of Origin 2017": "KST",
	"Liga Latinoamérica Norte": "PST",
	"Liga Latinoamérica": "PST",
	"Logitech Challenge Brasil": "CET",
	"LoL Champions Korea": "KST",
	"LoL Continental League": "CET",
	"LoL Development League": "KST",
	"LoL European Championship": "CET",
	"LoL Japan League": "KST",
	"LoL Master Series": "KST",
	"LoL Secondary Pro League": "KST",
	"LoL The Champions": "KST",
	"Major League Gaming": "PST",
	"Mid-Season Cup 2020": "KST",
	"Mid-Season Invitational": "International",
	"NA Academy League": "PST",
	"National Electronic Sports Tournament": "KST",
	"NiceGameTV LoL Battle": "KST",
	"North America Challenger Series": "PST",
	"North America League Championship Series": "PST",
	"Oceanic Challenger Series": "KST",
	"Oceanic Pro League": "KST",
	"PCS": "KST",
	"PGL": "CET",
	"Rift Rivals 2017 LLN-CLS-CBLOL": "PST",
	"Rift Rivals 2017 GPL-LJL-OPL": "KST",
	"Rift Rivals 2017 LCL-TCL": "CET",
	"Rift Rivals 2017 LCK-LPL-LMS": "KST",
	"Rift Rivals 2017 NA-EU": "International",
	"Riot Games": "International",
	"SK Telecom LTE-A LoL Masters": "KST",
	"SLTV StarSeries": "CET",
	"Tencent LoL Pro League": "KST",
	"Turkish Championship League": "CET",
	"Turkish Promotion League": "CET",
	"Turkey Academy League": "CET",
	"Vietnam Championship Series": "KST",
	"World Championship": "International",
	"World Cyber Arena": "KST",
	"Xtreme League": "CET",
}

class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if template.has('closest_timezone'):
			return
		if not template.has('CM_StandardLeague'):
			return
		league_input = template.get('CM_StandardLeague').value.strip()
		self.site: EsportsClient
		league = self.site.cache.get('League', league_input, 'long')
		if league not in leagues:
			return
		template.add('closest_timezone', leagues[league])


TemplateModifier(site, 'Infobox Tournament',
                 startat_page='Challengers Korea/2015 Season/Summer',
                 summary=summary).run()
