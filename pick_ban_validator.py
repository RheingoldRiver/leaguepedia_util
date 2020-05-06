from mwparserfromhell import parse
from mwparserfromhell.nodes import Template
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.esports_lookup_cache import EsportsLookupCache

CHAMPION_ARGS = [ 'blueban1', 'blueban2', 'blueban3', 'blueban4', 'blueban5', 'red_ban1', 'red_ban2', 'red_ban3', 'red_ban4', 'red_ban5', 'bluepick1', 'bluepick2', 'bluepick3', 'bluepick4', 'bluepick5', 'red_pick1', 'red_pick2', 'red_pick3', 'red_pick4', 'red_pick5' ]

ROLE_ARGS_BLUE = [ 'bluerole1', 'bluerole2', 'bluerole3', 'bluerole4', 'bluerole5' ]
ROLE_ARGS_RED = [ 'red_role1', 'red_role2', 'red_role3', 'red_role4', 'red_role5' ]

VALUES_TO_IGNORE = ['', 'unknown', 'none', 'missing data', 'loss of ban']


class PickBanValidator(object):
	def __init__(self, site:EsportsClient):
		self.site = site
		self.cache: EsportsLookupCache = site.cache
		self.recognized_templates = ['PicksAndBansS7', 'PicksAndBans']
	
	def has_champion_error(self, template):
		values = self._get_values_to_check(CHAMPION_ARGS, template)
		if self._check_for_duplicates(values, 'Champion', length='link'):
			return True
		return False
	
	def has_role_error(self, template):
		values = self._get_values_to_check(ROLE_ARGS_BLUE, template)
		if len(values) > 0 and len(values) != 5:
			return True
		if self._check_for_duplicates(values, 'Role', length='role'):
			return True
		values = self._get_values_to_check(ROLE_ARGS_RED, template)
		if len(values) > 0 and len(values) != 5:
			return True
		if self._check_for_duplicates(values, 'Role', length='role'):
			return True
		return False
	
	@staticmethod
	def _get_values_to_check(arg_list, template):
		values = []
		for arg in arg_list:
			if template.has(arg):
				value = template.get(arg).value.strip()
				if value != '':
					values.append(value)
		return values
	
	def _check_for_duplicates(self, values, file, length="link"):
		already_seen = []
		for i, value in enumerate(values):
			new = self.cache.get(file, value, length)
			if new in already_seen:
				return True
			already_seen.append(self._escape_value(value, i))
		return False
	
	@staticmethod
	def _escape_value(value, i):
		if value.lower() in ["none", "loss of ban", "unknown", "missing data"]:
			return value + "_" + str(i)
		return value

if __name__ == '__main__':
	credentials = AuthCredentials(user_file="me")
	site = EsportsClient('lol', credentials=credentials) # Set wiki
	validator = PickBanValidator(site)
	page = site.client.pages['Brazilian Challenger Circuit/2020 Season/Split 1/Picks and Bans/Week 5-7']
	text = page.text()
	wikitext = parse(text)
	for template in wikitext.filter_templates():
		if validator.has_champion_error(template):
			template.add('haschampionerror','Yes')
		if validator.has_role_error(template):
			template.add('hasroleerror','Yes')
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary='Detecting pick-ban error')
	else:
		print('Skipping page %s...' % page.name)
