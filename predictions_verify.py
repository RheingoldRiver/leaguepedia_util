from log_into_wiki import login

def run(site, revs):
	error_page = site.pages['User:RheingoldRiver/Prediction Reports']
	for rev in revs:
		if not rev['title'].startswith('Predictions:'):
			continue
		if "prediction_edit" in rev['tags']:
			continue
		error_page.append('\n[[Special:Diff/{}|{}]]<br>'.format(rev['revid'], rev['user']),
		                  summary="reporting possible cheating prediction!")
		

if __name__ == '__main__':
	site = login('me', 'lol')
	revs = site.recentchanges_by_interval(15)
	run(site, revs)
