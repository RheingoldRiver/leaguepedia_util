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
	                              prop='title|ids', **kwargs):
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
	
	def logs_by_interval(self, minutes, offset=0,
	                     lelimit="max",
	                     leprop='details|type|title', **kwargs):
		now = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset)
		then = now - datetime.timedelta(minutes=minutes)
		print(now)
		print(then)
		logs = self.api('query', format='json',
		                    list='logevents',
		                    # lestart=now.isoformat(),
		                    leend=then.isoformat(),
		                    leprop=leprop,
		                    lelimit="max",
	                        ledir='older',
	                        **kwargs
		                )
		return logs['query']['logevents']

	def patrol_recent(self, interval, f, **kwargs):
		revisions = self.recentchanges_by_interval(interval, prop='title|ids|patrolled', **kwargs)
		patrol_token = self.get_token('patrol')
		for revision in revisions:
			# revid == 0 if the page was deleted, so it can't be deleted
			if f(revision) and revision['revid'] != 0 and 'unpatrolled' in revision:
				self.api('patrol', revid = revision['revid'], token = patrol_token)

class GamepediaSite(ExtendedSite):
	def __init__(self, user, wiki, stg=False):
		suffix = 'io' if stg else 'com'
		super().__init__('%s.gamepedia.' % wiki + suffix, path='/')
		pwd_file = 'password2.txt' if user == 'bot' else 'password.txt'
		user_file = 'username2.txt' if user == 'bot' else 'username.txt'
		pwd = open(pwd_file).read().strip()
		username = open(user_file).read().strip()
		self.login(username, pwd)
