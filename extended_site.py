import mwclient

class ExtendedSite(mwclient.Site):
	def cargoquery(self, **kwargs):
		response = self.api('cargoquery', **kwargs)
		ret = []
		for item in response['cargoquery']:
			ret.append(item['title'])
		return ret
	
	def cargo_pagelist(self, fieldname, page_pattern = "%s", **kwargs):
		response = self.api('cargoquery', **kwargs)
		ret = []
		for item in response['cargoquery']:
			page = page_pattern % item['title'][fieldname]
			ret.append(self.pages[page])
		return ret
