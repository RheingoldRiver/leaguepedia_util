from log_into_wiki import login

def run(site, revs):
	error_page = site.pages['Log:Prediction Reports']
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
	site = login('me', 'lol')
	revs = site.recentchanges_by_interval(1)
	run(site, revs)
