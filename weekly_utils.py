import dateutil.parser, pytz, re, datetime, mwparserfromhell
import dateutil
from log_into_wiki import *

site = login('me','lol')

typo_find = ['favourite','quater','partecipate','Portugese', 'Regelations']
typo_replace = ['favorite','quarter','participate','Portuguese', 'Relegations']

def typoFixes(text):
	i = 0
	while i < len(typo_find):
		text = text.replace(typo_find,typo_replace)
	return text


teamhist_find = [r"(\d+)(\s*)-(\s*)(\"?Present\"?|''Present'')",
			   r'^\s*(.*)(\d+)\s*-\s*(\w+)',
			   r'^\s*(\w\w\w)(?:[A-Za-z])*\s*(\d\d\d\d) - (\w\w\w)(?:[A-Za-z])*\s*(\d)',
			   r"^\s*(\w\w\w)(?:[A-Za-z])*\s*(\d\d\d\d) - ''Present''",
			   r"^\s*(\w\w\w)(?:[A-Za-z])*\s*- (\w\w\w)(?:[A-Za-z])*\s*(\d\d\d\d)",
			   r"\?\s*-\s*Present",
			   r'^\s*([\? ]+)-',
			   r'^\s*(.*)-([\? ]+)$',
			   ]
teamhist_replace = [r"\1 - ''Present''",
				  r'\1\2 - \3',
				  r'\1 \2 - \3 \4',
				  r"\1 \2 - ''Present''",
				  r'\1 \3 - \2 \3',
				  r"? - ''Present''",
				  r'??? ???? -',
				  r'\1- ??? ????',
				  ]

social_fr = [
	{ "field" : "twitter", "find" : r'(?:\[?https?://)?(?:www\.)?(?:twitter\.com/)?([^/ \n]+)(.*\])?', "replace" : r'\1' },
	{ "field" : "twitter", "find" : r'/$', "replace" : r'' },
	{ "field" : "stream", "find" : r'\[?(?:https?://)?(.*)/([^ \n]+).*', "replace" : r'https://\1/\2' },
	{ "field" : "stream", "find" : r'/$', "replace" : r'' },
	{ "field" : "instagram", "find" : r'(?:\[?https?://)?(?:www\.)?(?:instagram\.com/)?([^/ \n]+)(.*\])?', "replace" : r'\1' },
	{ "field" : "instagram", "find" : r'/$', "replace" : r'' },
	{ "field" : "facebook", "find" : r'\[?(?:https?://)?(.*)/([^ \n]+).*', "replace" : r'https://\1/\2' },
	{ "field" : "facebook", "find" : r'/$', "replace" : r'' },
	{ "field" : "youtube", "find" : r'\[?(?:https?://)?([^ \n]*)(.*\])?', "replace" : r'https://\1' },
	{ "field" : "website", "find" : r'\[?([^ \n]*)(.*\])?', "replace" : r'\1' },
	{ "field" : "vk", "find": r'(?:\[?https?://)?(?:www\.)?(?:vk\.com/)?([^/ \n]+)(.*\])?', "replace": r'https://vk.com/\1'},
	{ "field" : "vk", "find" : r'/$', "replace" : r'' },
]

def fixSocialField(template, item):
	field = item['field']
	if template.has(field):
		val_old = template.get(field).value.strip()
		if val_old != '':
			val_arr = re.split(r'(<!--|-->)', val_old)
			val_arr[0] = re.sub(item['find'], item['replace'], val_arr[0])
			val_new = ''.join(val_arr)
			template.add(field, val_new)
			
def fixInfoboxPlayer(template):
	for item in social_fr:
		fixSocialField(template, item)
	i = 1
	key = 'teamdate' + str(i)
	while template.has(key):
		teamdate_new = str(template.get(key).value.strip())
		for j, f in enumerate(teamhist_find):
			teamdate_new = re.sub(f,teamhist_replace[j],teamdate_new)
		template.add(key,teamdate_new)
		i += 1
		key = 'teamdate' + str(i)
	return

def fixInfoboxTeam(template):
	for item in social_fr:
		fixSocialField(template, item)
	if template.has('isdisbanded'):
		if template.get('isdisbanded').value.strip().lower() == 'no':
			template.remove('isdisbanded')
	return

def createResults(site, page, template, subpage, result_type, template_text):
	if template.has('checkboxIsPersonality') and template.get('checkboxIsPersonality').value.strip() == 'Yes':
		pass
	else:
		p = site.pages[page + '/' + subpage]
		text = p.text()
		if text == '':
			p.save('{{{{{}TabsHeader}}}}\n{}'.format(result_type, template_text),tags='daily_errorfix')


pst = pytz.timezone('America/Los_Angeles')
est = pytz.timezone('America/New_York')
cet = pytz.timezone('Europe/Berlin')
kst = pytz.timezone('Asia/Seoul')
tz_lookup = {
	'PST' : pst,
	'EST' : est,
	'CET' : cet,
	'KST' : kst
}

def fixDST(template):
	if template.has('date') and template.has('time'):
		date = template.get("date").value.strip()
		time = template.get("time").value.strip()
		tz_local_str = template.get('timezone').value.strip()
		tz_local = tz_lookup[tz_local_str]
		date_time = dateutil.parser.parse(date + " " + time)
		date_time_local = tz_local.localize(date_time)
		isDST_PST = bool(date_time_local.astimezone(pst).dst())
		isDST_CET = bool(date_time_local.astimezone(cet).dst())
		if isDST_PST and isDST_CET:
			template.add('dst','yes')
		elif isDST_PST:
			template.add('dst','spring')
		else:
			template.add('dst','no')

def updateParams(template):
	# update gameschedule params for new conventions
	if template.has('t1score'):
		template.get('t1score').name = 'team1score'
	if template.has('t2score'):
		template.get('t2score').name = 'team2score'
	if template.has('post-match'):
		template.get('post-match').name = 'reddit'

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
			disablelimitreport = 1,
			wrapoutputclass = ''
		)
		result = query_result['parse']['text']['*']
		result = result.replace('<p>','').replace('\n</p>','')
		result_tbl = result.split(',')
		result_parsed = [x for x in result_tbl if x.lower() not in pb_exceptions]
		if len(result_parsed) != len(set(result_parsed)):
			template.add('has' + datatype + 'error','Yes')

def set_initial_order(wikitext):
	i = 0
	for template in wikitext.filter_templates():
		if template.name.matches('MatchSchedule/Start'):
			i = 0
			continue
		if template.name.matches('MatchSchedule'):
			i += 1
			if template.has('initialorder'):
				continue
			template.add('initialorder', str(i), before = 'team1')

DOC_PAGES_TO_MAKE = [
	{
		'matches': r'^Module:Bracket/',
		'notmatches': r'(doc|Wiki)$',
		'pages': {
			'Tooltip:Module:{}' : '{{BracketTooltip}}',
			'Module:{}/doc' : '{{BracketDoc}}'
		}
	},
	{
		'matches': r'^Module:.*/i18n$',
		'notmatches': r'doc$',
		'pages': {
			'Module:{}/doc': '{{i18ndoc}}'
		}
	},
	{
		'matches': r'^Module:CargoDeclare/',
		'notmatches': r'doc$',
		'pages': {
			'Module:{}/doc': '{{CargodocModule}}'
		}
	}
]

def make_doc_pages(site, p):
	for case in DOC_PAGES_TO_MAKE:
		if 'matches' in case.keys():
			if not re.findall(case['matches'], p.name):
				continue
		if 'notmatches' in case.keys():
			if re.findall(case['notmatches'], p.name):
				continue
		for i, (k, v) in enumerate(case['pages'].items()):
			site.pages[k.format(p.page_title)].save(v, summary='Automated error fixing (Python)',
									   tags='daily_errorfix')
