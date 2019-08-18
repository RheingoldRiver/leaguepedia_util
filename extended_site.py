import mwclient, datetime

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
	
	def recentchanges_by_interval(self, interval, offset=0, **kwargs):
		now = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset)
		then = now - datetime.timedelta(minutes=interval)
		result = self.recentchanges(
			start=now.isoformat(),
			end=then.isoformat(),
			limit='max',
			**kwargs
		)
		return result
	
	def patrol_recent(self, interval, f, **kwargs):
		revisions = self.recentchanges_by_interval(interval, prop='title|ids|patrolled', **kwargs)
		patrol_token = self.get_token('patrol')
		for revision in revisions:
			# revid == 0 if the page was deleted, so it can't be deleted
			if f(revision) and revision['revid'] != 0 and 'unpatrolled' in revision:
				self.api('patrol', revid = revision['revid'], token = patrol_token)
