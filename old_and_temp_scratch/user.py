import mwclient.errors
from mwclient.util import parse_timestamp

class User(object):
	def __init__(self, site, name, info=None):
		self.site = site
		self.name = name
		
		if not info:
			prop = 'blockinfo|groups|rights|editcount|registration|emailable'
			info = self.site.get('query', list='users', usprop=prop, ususers=name)
		info = info['query']['users'][0]
		
		self._info = info
		if 'invalid' in info:
			raise mwclient.errors.InvalidPageTitle(info.get('invalidreason'))
		
		self.id = info.get('userid')
		self.editcount = info.get('editcount', 0)
		self.registration = parse_timestamp(info.get('registration'))
		self.groups = info.get('groups', [])
		self.rights = info.get('rights', [])
		self.emailable = info.get('emailable')
	
	def can(self, right):
		return right in self.rights
	
	def in_group(self, group):
		return group in self.groups
	
	def add_rights(self, rights):
		self.change_rights(add=rights)
	
	def remove_rights(self, rights):
		self.change_rights(remove=rights)
	
	def change_rights(self, add=None, remove=None):
		if add is None:
			add = []
		if remove is None:
			remove = []
		
		to_add = '|'.join(add)
		to_remove = '|'.join(remove)
		self.site.post('userrights', user=self.name,
					   add=to_add, remove=to_remove,
					   token=self.site.get_token('userrights'))
	
	def clone_rights(self, new_site):
		rights = '|'.join(self.rights)
		new_site.post('userrights', user=self.name,
					  add=rights, token=new_site.get_token('userrights'))
		
	def remove_all_rights(self):
		self.remove_rights(self.groups)
