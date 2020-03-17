import re
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

def teamnames(site: EsportsClient):
	prefix_text = site.client.pages['Module:Team'].text()
	processed = prefix_text.replace('\n','')
	prefix = re.match(r".*PREFIX = '(.+?)'.*", processed)[1]
	site.client.api(
		action='parse',
		text='{{#invoke:CacheUtil|resetAll|Teamnames|module=Team|f=teamlinkname|prefix=' + prefix + '}}'
	)
