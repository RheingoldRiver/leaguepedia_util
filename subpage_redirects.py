from log_into_wiki import login

def run(site, logs):
	for log in logs:
		if 'mw-new-redirect' not in log['tags']:
			continue
