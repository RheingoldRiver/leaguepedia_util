import re
from river_mwclient.esports_site import EsportsSite

def teamnames(site: EsportsSite):
	prefix_text = site.client.pages['Module:Team'].text()
	processed = prefix_text.replace('\n','')
	prefix = re.match(r".*PREFIX = '(.+?)'.*", processed)[1]
	site.client.api(
		action='parse',
		text='{{#invoke:CacheUtil|resetAll|Teamnames|module=Team|f=teamlinkname|prefix=' + prefix + '}}'
	)
