from extended_site import GamepediaSite

class EsportsSite(GamepediaSite):
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
