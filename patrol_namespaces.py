from esportswiki_editing import *

namespaces = ['User:', 'Predictions:']

def run(site, revisions):
		patrol_token = site.get_token('patrol')
		for revision in revisions:
			# revid == 0 if the page was deleted, so it can't be deleted
			if do_we_patrol(revision) and revision['revid'] != 0 and 'unpatrolled' in revision:
				site.api('patrol', revid = revision['revid'], token = patrol_token)

def do_we_patrol(revision):
	return [_ for _ in namespaces if revision['title'].startswith(_)]

if __name__ == '__main__':
	site = login('me', 'lol')
	run(site, site.recentchanges_by_interval(200))
