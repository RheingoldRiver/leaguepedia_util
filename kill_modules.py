from log_into_wiki import *
import mwparserfromhell

site = login('me', 'fifa-esports')  # Set wiki
summary = 'Bot Edit'  # Set summary

pages_array = [
"Module:CurrentLeagueParticipantNavbox",
"Module:DPLUtil",
"Module:ExtendedRosterLine",
"Module:FeaturedLeagues",
"Module:FeaturedLeagues/Settings",
"Module:Flagnames",
"Module:FormUtil",
"Module:GetEventPageInfo",
"Module:HTMLUtil",
"Module:Infobox",
"Module:Infobox/Player",
"Module:Infobox/Social",
"Module:Infobox/Team",
"Module:Infobox/TeamHist",
"Module:InfoboxUtil",
"Module:Leaguestyles",
"Module:NavboxUtil",
"Module:OrgNavbox",
"Module:Placementnames",
"Module:Placementstrings",
"Module:PlayerListChart",
"Module:ProcessArgs",
"Module:Region",
"Module:Regionnames",
"Module:Regionstyles",
"Module:ReturnData",
"Module:Role",
"Module:Rolenames",
"Module:Rolestyles",
"Module:SpoilerFreeSchedule",
"Module:SubpageAfter",
"Module:SubpageNavbox",
"Module:SubpageSettings",
"Module:SubpageTabs",
"Module:Systems",
"Module:TableUtil",
"Module:TabsHeader",
"Module:Team",
"Module:TeamImage",
"Module:Teamexceptions",
"Module:Teamexceptionstyles",
"Module:Teamnames",
"Module:Teamstyles",
"Module:Text",
"Module:TimeUtil",
"Module:TitleUtil",
"Module:TournamentSection",
"Module:TournamentTabs",
"Module:Util",
"Module:Wiki",
"Module:Wikinames"]

token = site.get_token('csrf')

for page in pages_array:
	print(page)
	site.api('edit', format='json',
			 title=page,
			 contentmodel="Scribunto",
			 token= token,
			 appendtext = ''
			 )