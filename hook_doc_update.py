import re, mwparserfromhell
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

interval = 180

pattern_add = r'Hook.add\([\'"](\w+).*\)'
pattern_run = r'Hook.run\([\'"](\w+).*\)'

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki

revisions = site.recentchanges_by_interval(interval, toponly=1)

def add_missing_params(template, params_to_add):
	n = 0
	for param in template.params:
		n += 1
		param_str = str(param.value)
		if param_str in params_to_add:
			params_to_add.remove(param_str)
	for param in params_to_add:
		template.add(n + 1, param)
	params_to_add.clear()
	

def add_new_template(text, template_name, params):
	if not len(params):
		return text
	template = mwparserfromhell.nodes.Template(template_name)
	n = 1
	for param in params:
		template.add(n, param)
		n += 1
	if text == '':
		return str(template)
	return text + '\n' + str(template)

for revision in revisions:
	title = revision['title'].replace('/doc', '')
	if not title.startswith('Module:'):
		continue
	module = site.client.pages[title]
	doc = site.client.pages[title + '/doc']
	text = module.text()
	added = set()
	run = set()
	for match in re.findall(pattern_add, text):
		added.add(match)
	for match in re.findall(pattern_run, text):
		run.add(match)
	doc_text = doc.text()
	wikitext = mwparserfromhell.parse(doc_text)
	for template in wikitext.filter_templates():
		if template.name.matches('HooksAdded'):
			add_missing_params(template, added)
		elif template.name.matches('HooksRun'):
			add_missing_params(template, run)
	new_doc_text = str(wikitext)
	new_doc_text = add_new_template(new_doc_text, 'HooksAdded', added)
	new_doc_text = add_new_template(new_doc_text, 'HooksRun', run)
	if new_doc_text != '' and (doc_text == '' or not doc_text):
		new_doc_text = '<includeonly>{{luadoc}}[[Category:Lua Modules]]</includeonly>\n' + new_doc_text
	if new_doc_text and doc_text != new_doc_text and new_doc_text.strip() != '':
		doc.save(new_doc_text, summary="Auto updating hook documentation page")
