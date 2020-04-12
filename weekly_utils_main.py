# weekly is a lie, this runs twice-daily

import mwparserfromhell, datetime
import weekly_utils as utils
import scrape_runes
from pick_ban_validator import PickBanValidator
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
pick_ban_validator = PickBanValidator(site)

limit = -1

now_timestamp = datetime.datetime.utcnow().isoformat()
with open('daily_last_run.txt','r') as f:
	last_timestamp = f.read()
with open('daily_last_run.txt','w') as f:
	f.write(now_timestamp)

revisions = site.client.api('query', format='json',
					 list='recentchanges',
					 rcstart=now_timestamp,
					 rcend=last_timestamp,
					 rcprop='title|ids|patrolled',
					 rclimit='max',
					 rctoponly=1, # commented bc we need all revisions to patrol user pages
					 rcdir = 'older'
					 )

pages = []
pages_for_runes = []

def report_errors(report_page, page, errors):
	text = report_page.text()
	error_text = '\n* '.join([e.args[0] for e in errors])
	newtext = text + '\n==Python Error Report==\nPage: [[{}]] Messages:\n* {}'.format(page, error_text)
	report_page.save(newtext)

for revision in revisions['query']['recentchanges']:
	title = revision['title']
	if title not in pages:
		pages.append(title)
		if title.startswith('Data:'):
			pages_for_runes.append(title)

lmt = 1
for page in pages:
	if lmt == limit:
		break
	lmt+=1
	try:
		p = site.client.pages[page]
	except KeyError:
		# print(page)
		continue
	else:
		text = p.text()
		wikitext = mwparserfromhell.parse(text)
		errors = []
		for template in wikitext.filter_templates():
			try:
				if template.name.matches('Infobox Player'):
					utils.fixInfoboxPlayer(template)
				elif template.name.matches('Infobox Team'):
					utils.fixInfoboxTeam(template)
				elif template.name.matches('PicksAndBansS7') or template.name.matches('PicksAndBans'):
					utils.fixPB(pick_ban_validator, template)
				elif template.name.matches('Listplayer/Current/End'):
					template.add(1, '')
			except Exception as e:
				errors.append(e)
		newtext = str(wikitext)
		if text != newtext:
			# print('Saving page %s...' % page)
			p.save(newtext,summary='Automated error fixing (Python)',tags='daily_errorfix')
		if len(errors) > 0:
			report_page = site.client.pages['User talk:RheingoldRiver']
			report_errors(report_page, page, errors)

success_page = site.client.pages['User:RheingoldRiver/Maint Log']
text = success_page.text()
text = text + '\nScript finished maint successfully: ' + now_timestamp
try:
	scrape_runes.scrape(site, pages_for_runes, False)
	text = text + '\nScript finished regular runes successfully: ' + now_timestamp
except Exception as e:
	text = text + '\nException running regular runes: ' + str(e) + ' ' + now_timestamp
try:
	scrape_runes.scrapeLPL(site, pages_for_runes, False)
	text = text + '\nScript finished everything successfully: ' + now_timestamp
except Exception as e:
	text = text + '\nException running LPL runes: ' + str(e) + ' ' + now_timestamp
success_page.save(text,tags='daily_errorfix')
