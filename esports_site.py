from extended_site import GamepediaSite

ALL_ESPORTS_WIKIS = ['lol', 'halo', 'smite', 'vg', 'rl', 'pubg', 'fortnite',
					 'apexlegends', 'fifa', 'gears', 'nba2k', 'paladins', 'siege',
					 'default-loadout', 'commons', 'teamfighttactics']

def get_wiki(wiki):
	if wiki in ['lol', 'teamfighttactics']:
		return wiki
	return wiki + '-esports'

class EsportsSite(GamepediaSite):
	def __init__(self, user, wiki):
		super().__init__(user, get_wiki(wiki))
		self.user = user
		self.wiki = wiki
	
	def standard_name_redirects(self):
		for item in self.cargoquery(
			tables="Tournaments,_pageData",
			join_on="Tournaments.StandardName_Redirect=_pageData._pageName",
			where="_pageData._pageName IS NULL AND Tournaments.StandardName_Redirect IS NOT NULL",
			fields="Tournaments.StandardName_Redirect=Name,Tournaments._pageName=Target",
			limit="max"
		):
			page = self.pages[item['Name']]
			target = item['Target']
			page.save('#redirect[[%s]]' % target, summary="creating needed CM_StandardName redirects")
	
	def other_wikis(self):
		for wiki in ALL_ESPORTS_WIKIS:
			if wiki == self.wiki:
				continue
			yield wiki
	
	def other_sites(self):
		for wiki in self.other_wikis():
			yield EsportsSite('me', wiki)
	
	@staticmethod
	def all_wikis():
		for wiki in ALL_ESPORTS_WIKIS:
			yield wiki
	
	@staticmethod
	def all_sites(user):
		for wiki in ALL_ESPORTS_WIKIS:
			yield EsportsSite(user, wiki)
