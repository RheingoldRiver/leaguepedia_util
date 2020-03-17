from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

def run(site, revs):
	error_page = site.client.pages['Log:Prediction Reports']
	for rev in revs:
		if not rev['title'].startswith('Predictions:'):
			continue
		if "prediction_edit" in rev['tags']:
			continue
		# ignore if it's a deletion
		if rev['revid'] == 0:
			continue
		error_page.append('\n[[Special:Diff/{}|{}]]<br>'.format(rev['revid'], rev['user']),
		                  summary="reporting possible cheating prediction!")
		

if __name__ == '__main__':
	site = EsportsClient('lol')
	site.client.login_from_file('me')
	revs = site.client.recentchanges_by_interval(100)
	run(site, revs)
