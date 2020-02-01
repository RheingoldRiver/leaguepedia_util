from log_into_wiki import login


class CronTasks(object):
	def __init__(self, interval=1, wikis=None):
		self.all_wikis = wikis
		self.all_sites = {}
		self.all_revs = {}
		self.all_logs = {}
		for wiki in self.all_wikis:
			site = login('me', wiki)
			revs_gen = site.recentchanges_by_interval(interval)
			revs = [_ for _ in revs_gen]
			logs = site.logs_by_interval(interval)
			self.all_sites[wiki] = site
			self.all_revs[wiki] = revs
			self.all_logs[wiki] = logs
	
	def run_logs(self, fn, wikis, **kwargs):
		self._run_data(fn, wikis, self.all_logs, **kwargs)
	
	def run_revs(self, fn, wikis, **kwargs):
		self._run_data(fn, wikis, self.all_revs, **kwargs)
	
	def _run_data(self, fn, wikis, data, **kwargs):
		if wikis is None:
			return
		for wiki in wikis:
			try:
				fn(self.all_sites[wiki], data[wiki], **kwargs)
			except Exception as e:
				print(e)
				pass
