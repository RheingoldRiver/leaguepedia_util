from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials


class CronTasks(object):
	"""Handles scheduling cron tasks that run based on sites' revisions and/or logs
	
	Initialize with number of minutes and set of wikis to create lists for, then
	run the tasks that you want run with run_logs or run_revs.
	Does NOT support running code that requires seeing both - in cases like that, separate
	the functionality into 2 separate functions.
	The set of wikis you run each individual task on will often be a subset of the total
	set of wikis, so re-specify that for each function defined.
	Use one file per interval because that's convenient for cron scheduling.
	"""
	def __init__(self, interval=1, wikis=None):
		self.all_wikis = wikis
		self.all_sites = {}
		self.all_revs = {}
		self.all_logs = {}
		for wiki in self.all_wikis:
			credentials = AuthCredentials(user_file="me")
			site = EsportsClient('lol', credentials=credentials)  # Set wiki
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
			site = self.all_sites[wiki]
			try:
				fn(site, data[wiki], **kwargs)
			except Exception as e:
				site.log_error_script(error=e)
			site.report_all_errors('Cron Errors (%s)' % fn.__module__)
