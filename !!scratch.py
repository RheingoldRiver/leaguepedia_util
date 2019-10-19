from esports_site import EsportsSite

pages = [
"Module:ScoreboardPlayerStats",
"Module:ExtendedRosterLine",
"Module:Scoreboard",
"Module:Standings",
"Module:Timeline",
"Module:Crossbox",
"Module:MatchList",
"Module:CargoUtil",
"Module:RosterTooltip",
"Module:DisambigPage",
"Module:ArgsUtil",
"Module:FootnoteUtil",
"Module:PickBanHistory",
"Module:CastingHistory",
"Module:TeamPLHQuery",
"Module:I18nUtil",
"Module:MatchDetails",
"Module:MatchSchedule",
"Module:MatchCalendarExport",
"Module:PlayerPentakills",
"Module:PlayerResults1v1",
"Module:UserPredictionsLeaderboard",
"Module:CargoDeclare",
"Module:RosterChangeData",
"Module:LeaguesNavbox",
"Module:NewsQueryAbstract",
"Module:ExternalContentQueryBase",
"Module:SourceUtil",
]

site = EsportsSite('me', 'lol')

for p in pages:
	page = site.pages[p]
	text = page.text()
	split_str = text.split('util_table.map')
	split_str = [_[0].lower() + _[1:] for _ in split_str]
	new_text = 'util_map.'.join(split_str)
	if new_text != text:
		page.save(new_text, summary = 'Use MapUtil instead of TableUtil for mapping functions')
