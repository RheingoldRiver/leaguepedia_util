from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials

def run(site: EsportsClient, logs):
	for log in logs:
		if 'mw-new-redirect' not in log['tags']:
			continue

if __name__ == '__main__':
	credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
