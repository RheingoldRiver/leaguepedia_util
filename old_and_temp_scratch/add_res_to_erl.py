from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:News Navbox']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

def api_parse_query(site, datatype, values):
	query_text = '{{#invoke:PrintParsedText|unordered|type=' + datatype + '|' + '|'.join(values) + '}}'
	query_result = site.api(
		'parse',
		format='json',
		text=query_text,
		prop='text',
		disablelimitreport=1,
		wrapoutputclass=''
	)
	result = query_result['parse']['text']['*']
	result = result.replace('<p>', '').replace('\n</p>', '')
	result_tbl = result.split(',')
	return result_tbl

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		players_to_check = []
		for template in wikitext.filter_templates():
			if template.name.matches('TEMPLATEYOUCAREABOUT'):
				if template.has('res'):
					pass
				else:
					if template.has('link'):
						players_to_check.append(template.get('link').value.strip())
					elif template.has('player'):
						players_to_check.append(template.get('player').value.strip())
		reslist = api_parse_query(site, 'player_res', )
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)
