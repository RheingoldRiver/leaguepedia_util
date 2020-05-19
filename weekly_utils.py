import re
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki


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
	{ "field" : "youtube", "find" : r'\[?(?:https?://)?([^ \n]+)(.+\])?', "replace" : r'https://\1' },
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
			# This was added as a fix because youtube was adding random https:// at the end of everything
			# Maybe space and \n isn't sufficient whitespace to require a match actually be there
			# But it seems to work now
			# (the error was a python 3.5 -> 3.8 change, re was updated in 3.7, probably caused this)
			if val_arr[0].strip() != '':
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

def fixPB(validator, template):
	if validator.has_champion_error(template):
		template.add('haschampionerror','Yes')
	if validator.has_role_error(template):
		template.add('hasroleerror','Yes')
