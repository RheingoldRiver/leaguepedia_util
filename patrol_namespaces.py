from river_mwclient.esports_site import EsportsSite

namespaces = ['User:', 'Predictions:']

def run(site: EsportsSite, revisions):
		patrol_token = site.client.get_token('patrol')
		for revision in revisions:
			# revid == 0 if the page was deleted, so it can't be deleted
			if do_we_patrol(revision) and revision['revid'] != 0 and 'unpatrolled' in revision:
				site.client.api('patrol', revid = revision['revid'], token = patrol_token)

def do_we_patrol(revision):
	return [_ for _ in namespaces if revision['title'].startswith(_)]

if __name__ == '__main__':
	site = EsportsSite('lol', user_file="me")  # Set wiki
	run(site, site.client.recentchanges_by_interval(200))
