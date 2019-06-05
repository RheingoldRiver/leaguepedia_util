# weekly is a lie, this runs twice-daily

import mwparserfromhell, datetime
import weekly_utils as utils
import scrape_runes, luacache_refresh
from log_into_wiki import *
from template_list import *

site = login('me','lol')

limit = -1

# Blank edit pages we need to
blank_edit_pages = ['Leaguepedia:Top Schedule']
for page in blank_edit_pages:
	p = site.pages[page]
	p.save(p.text(), summary = 'blank editing')

now_timestamp = datetime.datetime.utcnow().isoformat()
with open('daily_last_run.txt','r') as f:
	last_timestamp = f.read()
with open('daily_last_run.txt','w') as f:
	f.write(now_timestamp)

revisions = site.api('query', format='json',
					 list='recentchanges',
					 rcstart=now_timestamp,
					 rcend=last_timestamp,
					 rcprop='title|ids|patrolled',
					 rclimit='max',
					 #rctoponly=0, # commented bc we need all revisions to patrol user pages
					 rcdir = 'older'
					 )

patrol_token = site.get_token('patrol')

pages = []
pages_for_runes = []

for revision in revisions['query']['recentchanges']:
	title = revision['title']
	# Patrol user namespace edits (not user talk)
	if (revision['ns'] == 2 or revision['ns'] == 10014) and 'unpatrolled' in revision:
		site.api('patrol', format = 'json',
				 revid = revision['revid'],
				 token = patrol_token
				 )
	if title not in pages:
		pages.append(title)
		if title.startswith('Data:'):
			pages_for_runes.append(title)

lmt = 1
for page in pages:
	if lmt == limit:
		break
	lmt+=1
	p = site.pages[page]
	if '/Edit Conflict/' in page and p.namespace == 2 and p.text() != '':
		p.delete(reason='Deleting old edit conflict')
	elif page.startswith('Module:Bracket/') and not (page.endswith('doc') or page.endswith('Wiki')):
		newpage = site.pages['Tooltip:' + page]
		newpage.save('{{BracketTooltip}}', summary='Automated error fixing (Python)',tags='daily_errorfix')
	elif page.endswith('/i18n') and page.startswith('Module'):
		newpage = site.pages[page + '/doc']
		if newpage.text() == '':
			newpage.save('{{i18ndoc}}',tags='daily_errorfix')
	else:
		text = p.text()
		wikitext = mwparserfromhell.parse(text)
		errors = []
		for template in wikitext.filter_templates():
			try:
				if template.name.matches('Infobox Player'):
					utils.fixInfoboxPlayer(template)
					if p.namespace == 0:
						if template.has('checkboxIsPersonality'):
							if template.get('checkboxIsPersonality').value.strip() != 'Yes':
								utils.createResults(site, page, template, 'Tournament Results', 'Player', '{{PlayerResults|show=everything}}')
				elif template.name.matches('Infobox Team'):
					utils.fixInfoboxTeam(template)
					if p.namespace == 0:
						utils.createResults(site, page, template, 'Tournament Results', 'Team', '{{TeamResults|show=everything}}')
						utils.createResults(site, page, template, 'Schedule History', 'Team', '{{TeamScheduleHistory}}')
						tooltip = site.pages['Tooltip:%s' % page]
						tooltip.save('{{RosterTooltip}}',tags='daily_errorfix')
				elif template.name.strip() in gameschedule_templates:
					utils.fixDST(template)
					utils.updateParams(template)
				elif template.name.matches('PicksAndBansS7') or template.name.matches('PicksAndBans'):
					utils.fixPB(site, template)
				elif template.name.matches('Listplayer/Current/End'):
					template.add(1, '')
			except Exception as e:
				errors.append(e)
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page)
			p.save(newtext,summary='Automated error fixing (Python)',tags='daily_errorfix')
		if len(errors) > 0:
			report_page = site.pages['User talk:RheingoldRiver']
			report_errors(report_page, page, errors)
luacache_refresh.teamnames(site)
success_page = site.pages['User:RheingoldRiver/Maint Log']
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