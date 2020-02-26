from river_mwclient.esports_site import EsportsSite
import mwparserfromhell
import json

site = EsportsSite('lol', user_file="me")  # Set wiki
summary = 'Add |same_page= param for renames'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'Data:News/2019-12-08'
this_template = site.client.pages['Template:ContractData']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

class Cache(object):
	def __init__(self, site: EsportsSite):
		self.cache = {}
		self.site = site
	
	def get_json_lookup(self, filename):
		if filename in self.cache:
			return self.cache[filename]
		result = self.site.client.api(
			'expandtemplates',
			prop='wikitext',
			text='{{JsonEncode|%s}}' % filename
		)
		self.cache[filename] = json.loads(result['expandtemplates']['wikitext'])
		return self.cache[filename]
	
	def get_value_from_lookup_json(self, filename, key, length):
		"""
		Returrns the length of the lookup of a key requested from the filename requested. Assumes the file has
		the same structure as the -names modules on Leaguepedia.
		:param filename: "Champion", "Role", etc. - the name of the file
		:param key: The lookup key, e.g. "Morde"
		:param length: The length of value to return, e.g. "long" or "link"
		:return: Correct lookup value provided, or None if it's not found
		"""
		key = key.lower()
		file = self.get_json_lookup(filename)
		if key not in file:
			return None
		if not isinstance(file[key], str):
			return file[key][length]
		return file[file[key]][length]
	
	def get_cargo_query(self, key, **kwargs):
		"""
		Cache results of a cargo query and return if needed
		:param key: A key to save this query as to look it up later without rerunning the query
		:param kwargs: Parameters for a cargoquery api call
		:return:
		"""
		if self.cache[key]:
			return self.cache[key]
		result = self.site.cargo_client.cargoquery(**kwargs)
		self.cache[key] = result
		return result

response = site.cargo_client.query(
	tables="TeamRenames=Renames,TeamRedirects=TR1,TeamRedirects=TR2",
	join_on="Renames.OriginalName=TR1.AllName,Renames.NewName=TR2.AllName",
	where='TR1._pageName=TR2._pageName AND (Renames.IsSamePage IS NULL or Renames.IsSamePage="0")',
	fields="Renames._pageName=Page,OriginalName,NewName",
	limit="max"
)

cache = Cache(site)

for item in response:
	page = site.client.pages[item['Page']]
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	print(item)
	for template in wikitext.filter_templates():
		if template.name.matches('TeamRename'):
			this_name = cache.get_value_from_lookup_json('Team', template.get('original').value.strip(), 'link')
			print(this_name)
			print(item['OriginalName'])
			if item['OriginalName'].strip() != this_name.strip():
				continue
			template.add('same_page', 'Yes')
	newtext = str(wikitext)
	if newtext != text:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
