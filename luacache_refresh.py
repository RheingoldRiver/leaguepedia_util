import re

def teamnames(site):
	prefix_text = site.pages['Module:Team'].text()
	processed = prefix_text.replace('\n','')
	prefix = re.match(r".*PREFIX = '(.+?)'.*", processed)[1]
	print('Prefix: %s' % prefix)
	site.api(
		action='parse',
		text='{{#invoke:CacheUtil|resetAll|Teamnames|module=Team|f=teamlinkname|prefix=' + prefix + '}}'
	)