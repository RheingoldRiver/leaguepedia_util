from river_mwclient.esports_site import EsportsSite

def run(site: EsportsSite, logs):
	for log in logs:
		if 'mw-new-redirect' not in log['tags']:
			continue

if __name__ == '__main__':
	site = EsportsSite('lol', user_file="me")  # Set wiki
