from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

namespaces = ['User:', 'Predictions:']

def run(site: EsportsClient, revisions):
		patrol_token = site.client.get_token('patrol')
		for revision in revisions:
			# revid == 0 if the page was deleted, so it can't be deleted
			if do_we_patrol(revision) and revision['revid'] != 0 and 'unpatrolled' in revision:
				site.client.api('patrol', revid = revision['revid'], token = patrol_token)

def do_we_patrol(revision):
	return [_ for _ in namespaces if revision['title'].startswith(_)]

if __name__ == '__main__':
	credentials = AuthCredentials(user_file="me")
	site = EsportsClient('lol', credentials=credentials)  # Set wiki
	run(site, site.recentchanges_by_interval(200))
