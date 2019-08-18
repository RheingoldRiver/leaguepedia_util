import log_into_wiki

namespaces = ['User:', 'Predictions:']
site_names = ['lol', 'cod-esports']
interval = 10

def do_we_patrol(revision):
	return [_ for _ in namespaces if revision['title'].startswith(_)]

for site_name in site_names:
	site = log_into_wiki.login('me', site_name)
	site.patrol_recent(interval, do_we_patrol)
