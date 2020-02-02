import mwclient, datetime

class ExtendedSite(mwclient.Site):
	def cargoquery(self, **kwargs):
		response = self.api('cargoquery', **kwargs)
		ret = []
		for item in response['cargoquery']:
			ret.append(item['title'])
		return ret

	def cargo_pagelist(self, fields=None, limit="max", page_pattern = "%s", **kwargs):
		field = fields.split('=')[1] if '=' in fields else fields
		group_by = fields.split('=')[0]
		response = self.api('cargoquery',
			fields=fields,
			group_by=group_by,
			limit=limit,
			**kwargs
		)
		pages = []
		for item in response['cargoquery']:
			page = page_pattern % item['title'][field]
			if page in pages:
				continue
			pages.append(page)
			yield(self.pages[page])

	def recentchanges_by_interval(self, minutes, offset=0,
	                              prop='title|ids|tags|user|patrolled'
	                              , **kwargs):
		now = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset)
		then = now - datetime.timedelta(minutes=minutes)
		result = self.recentchanges(
			start=now.isoformat(),
			end=then.isoformat(),
			limit='max',
			prop=prop,
			**kwargs
		)
		return result
	
	def recent_titles_by_interval(self, *args, **kwargs):
		revisions = self.recentchanges_by_interval(*args, **kwargs, toponly=0)
		titles = [_['title'] for _ in revisions]
		return titles
	
	def recent_pages_by_interval(self, *args, **kwargs):
		revisions = self.recent_titles_by_interval(*args, **kwargs)
		titles = [_['title'] for _ in revisions]
		for title in titles:
			yield self.pages[title]
	
	def logs_by_interval(self, minutes, offset=0,
	                     lelimit="max",
	                     leprop='details|type|title', **kwargs):
		now = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset)
		then = now - datetime.timedelta(minutes=minutes)
		logs = self.api('query', format='json',
		                    list='logevents',
		                    # lestart=now.isoformat(),
		                    leend=then.isoformat(),
		                    leprop=leprop,
		                    lelimit=lelimit,
	                        ledir='older',
	                        **kwargs
		                )
		return logs['query']['logevents']

class GamepediaSite(ExtendedSite):
	def __init__(self, user, wiki, stg=False):
		suffix = 'io' if stg else 'com'
		super().__init__('%s.gamepedia.' % wiki + suffix, path='/')
		pwd_file = 'password2.txt' if user == 'bot' else 'password.txt'
		user_file = 'username2.txt' if user == 'bot' else 'username.txt'
		pwd = open(pwd_file).read().strip()
		username = open(user_file).read().strip()
		self.login(username, pwd)
