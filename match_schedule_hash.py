import datetime
import mwparserfromhell
from log_into_wiki import *

ERROR_LOCATION = 'Maintenance:MatchSchedule Ordering Errors'
ERROR_TEAMS_TEXT = 'Team 1 - {}; Team 2: {}'

def get_append_hash(hash, res):
	tl = mwparserfromhell.nodes.Template(name='MSHash')
	tl.add('hash', hash)
	tl.add('team1', res['Team1'])
	tl.add('team2', res['Team2'])
	return str(tl)

def verify_hash(template, team1, team2):
	return template.get('team1').value.strip() == team1 and template.get('team2').value.strip() == team2

def get_hash_template(ms_hash, wikitext):
	for template in wikitext.filter_templates():
		if template.has('hash') and template.get('hash').value.strip() == ms_hash:
			return template
	return None
	
def get_error_text(res, page_name, tl):
	match_info = 'Page - [[{}]]; Tab - {}; initialorder: {}'.format(page_name, res['Tab'], res['Order'])
	original = ERROR_TEAMS_TEXT.format(tl.get('team1').value.strip(), tl.get('team2').value.strip())
	new = ERROR_TEAMS_TEXT.format(res['Team1'], res['Team2'])
	return 'Match Info: {}\n<br>Originally: {}\n<br>Now: {}<br>'.format(match_info, original, new)

def write_errors(site, errors):
	if len(errors) == 0:
		return
	page = site.pages[ERROR_LOCATION]
	if page.text() != '':
		errors.insert(0, page.text())
	text = '\n'.join(errors)
	page.save(text, summary = 'Reporting MatchSchedule initialorder Errors')

def check_page(site, page_name):
	response = site.api('cargoquery', tables = 'MatchSchedule',
					  fields = 'InitialN_MatchInTab=Order, Team1, Team2, Tab',
					  where = '_pageName="%s"' % page_name
					  )
	result = response['cargoquery']
	hash_location = site.pages[page_name + '/Hash']
	text = hash_location.text()
	wikitext = mwparserfromhell.parse(text)
	hashes_to_add = []
	errors = []
	for res in result:
		data = res['title']
		ms_hash = data['Tab'] + '_' + data['Order']
		hash_template = get_hash_template(ms_hash, wikitext)
		if not hash_template:
			hashes_to_add.append(get_append_hash(ms_hash, data))
		elif not verify_hash(hash_template, data['Team1'], data['Team2']):
			errors.append(get_error_text(data, page_name, hash_template))
			hash_template.add('team1', data['Team1'])
			hash_template.add('team2', data['Team2'])
		else:
			continue
	write_errors(site, errors)
	hashes_to_add.insert(0, str(wikitext))
	new_text = '\n'.join(hashes_to_add)
	if text != new_text:
		hash_location.save(new_text)

def check_recent_revisions(site):
	then_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=20)
	then = then_time.isoformat()
	now = datetime.datetime.utcnow().isoformat()
	revisions = site.api('query', format='json',
						 list='recentchanges',
						 rcstart=now,
						 rcend=then,
						 rcprop='title',
						 rclimit='max',
						 # rctoponly=0, # commented bc we need all revisions to patrol user pages
						 rcdir='older'
						 )
	titles = []
	for revision in revisions['query']['recentchanges']:
		if revision['title'].startswith('Data:'):
			titles.append(revision['title'])
	for title in titles:
		check_page(site, title)

if __name__ == '__main__':
	site = login('me', 'lol')
	check_recent_revisions(site)
