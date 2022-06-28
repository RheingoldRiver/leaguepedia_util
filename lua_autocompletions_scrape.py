from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)

pages = site.client.allpages(namespace=828)

for page in pages:
	text = page.text()
