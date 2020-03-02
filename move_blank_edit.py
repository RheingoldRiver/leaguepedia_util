from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

def run(site: EsportsClient, logs):
	for log in logs:
		if 'action' not in log.keys() or log['action'] != 'move':
			continue
		old_page_name = log['title']
		new_page_name = log['params']['target_title']
		if 'suppressredirect' not in log['params'].keys():
			site.client.pages[old_page_name].touch()
		new_page = site.client.pages[new_page_name]
		new_page.touch()
		new_page.touch()
		
	
if __name__ == '__main__':
	credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
	run(site, site.client.logs_by_interval(40))
