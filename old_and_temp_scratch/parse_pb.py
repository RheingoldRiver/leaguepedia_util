import mwparserfromhell, time, mwclient
from log_into_wiki import *
site = login('me','lol')

tl = site.pages['Module:PicksAndBans']
page_list = tl.embeddedin()

pages_var = list(page_list)

pages_array = [p for p in pages_var]
page_names = [p.name for p in pages_array]

try:
	startat = page_names.index('Season 2 World Championship/Picks and Bans/Group Stage')
except ValueError as e:
	startat = -1
print(startat)
limit = -1

pb_data = [
	{
		'data_type' : 'champion',
		'args' : [ 'blueban1', 'blueban2', 'blueban3', 'blueban4', 'blueban5', 'red_ban1', 'red_ban2', 'red_ban3', 'red_ban4', 'red_ban5', 'bluepick1', 'bluepick2', 'bluepick3', 'bluepick4', 'bluepick5', 'red_pick1', 'red_pick2', 'red_pick3', 'red_pick4', 'red_pick5' ]
	},
	{
		'data_type' : 'role',
		'args' : [ 'bluerole1', 'bluerole2', 'bluerole3', 'bluerole4', 'bluerole5' ],
	},
	{
		'data_type' : 'role',
		'args' : [ 'red_role1', 'red_role2', 'red_role3', 'red_role4', 'red_role5' ]
	}
]

pb_exceptions = ['', 'unknown', 'none', 'missing data', 'loss of ban']

def fixPB(site, template):
	for lookup in pb_data:
		values = []
		datatype = lookup['data_type']
		for arg in lookup['args']:
			if template.has(arg):
				values.append(template.get(arg).value.strip())
		query_text = '{{#invoke:PrintParsedText|unordered|type=' + datatype + '|' + '|'.join(values) + '}}'
		query_result = site.api(
			'parse',
			format = 'json',
			text = query_text,
			prop = 'text',
			disablelimitreport = 1
		)
		result = query_result['parse']['text']['*']
		result = result.replace('<p>','').replace('\n</p>','')
		result_tbl = result.split(',')
		result_parsed = [x for x in result_tbl if x.lower() not in pb_exceptions]
		if len(result_parsed) != len(set(result_parsed)):
			template.add('has' + datatype + 'error','Yes')

lmt = 0
for page in pages_array:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		pass
	else:
		print('Starting page %s...' % page.name)
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('PicksAndBansS7') or template.name.matches('PicksAndBans'):
				fixPB(site, template)
		newtext = str(wikitext)
		if newtext != text:
			try:
				print('Saving page %s...' % page.name)
				page.save(newtext,summary = 'Adding errors to pick-ban')
			except mwclient.errors.APIError as e:
				print('APIError, sleeping for 120 seconds...')
				time.sleep(120)
				print('Trying again...')
				page.save(newtext, summary='Adding errors to pick-ban')