import re, time, urllib.request, math

class TeamSpriteEntry(object):
	def __init__(self, pos, link=None, date=None, line=None, file=None):
		self.link = link
		self.pos = pos
		self.date = date
		self.file = file
		self.inactive = False
		if line:
			self.read_from_line(line)
	
	def force_inactive(self):
		self.inactive = True
	
	def set_date(self, date):
		self.date = date
		
	def set_link(self, link):
		self.link = link
	
	def set_file(self, file):
		self.file = file
	
	def read_from_line(self, line):
		if line != '':
			#print(line)
			self.link = re.search(r'\["(.*)"\]', line)[1].strip()
			if "permanent = true" in line:
				self.date = math.floor(time.time())
			else:
				self.date = re.search(r'date = (\d+)', line)[1].strip()
			self.file = re.search(r'file = "(.+?)"', line)[1].strip()
			#print(self.pos)
			#print('re result ' + re.search(r'pos = ([0-9]+)', line)[1].strip())
			assert(re.search(r'pos = ([0-9]+)', line)[1].strip() == str(self.pos + 1))
		
	def print_to_line(self):
		if self.link and self.date:
			return '\t\t["{}"] = {{ pos = {}, date = {}, file = "{}" }},\n'.format(self.link, self.pos + 1, self.date, self.file)
		else:
			return '\n'
	
	def is_currently_active(self):
		# active will mean used in the past 24 hours
		#print('checking activity %s' % self.link)
		if self.inactive:
			return False
		if self.is_empty():
			return False
		return math.floor(time.time()) - int(self.date) < 60 * 60 * 24
	
	def is_empty(self):
		return not self.link
	
	def destroy(self):
		self.link = None
		self.date = None
	
	def set_active(self):
		self.date = math.floor(time.time())
	
	def add_item(self, team):
		self.link = team
		self.set_active()

class SpriteSheet(object):
	def __init__(self, file):
		self.sprites_by_pos = []
		self.sprites_by_link = {}
		self.to_add = {}
		self.made_changes = False
		self.urls_used = []
		for i, line in enumerate(file.split('\n')):
			sprite = TeamSpriteEntry(i, line=line)
			self.sprites_by_pos.append(sprite)
			self.sprites_by_link[sprite.link] = sprite
			self.urls_used.append(sprite.file)
	
	def add_activity_from_wiki_page(self, site, page_name):
		to_parse_text = '{{:%s}}' % page_name
		result = site.api('expandtemplates', title = 'Main Page', text = to_parse_text, disablelimitreport = 1)
		text = result['expandtemplates']['*']
		#print(text)
		pattern = r'\[\[File:([^\]]+?)logo[ _]std\.png'
		key_list = re.findall(pattern, text)
		self.add_activity(key_list)
	
	def add_activity(self, key_list):
		for team in key_list:
			#print(team)
			#print(self.next_empty_node)
			key = team.replace('_',' ')
			if key in self.sprites_by_link:
				self.sprites_by_link[key].set_active()
			elif key in self.to_add:
				print('bunnies')
				pass
			else:
				print(key + ' key')
				self.made_changes = True
				print(self.find_next_empty_node())
				next_sprite = TeamSpriteEntry(self.find_next_empty_node(), link=key, date=math.floor(time.time()))
				self.to_add[key] = next_sprite
				if next_sprite.pos < len(self.sprites_by_pos):
					self.sprites_by_pos[next_sprite.pos] = next_sprite
				else:
					self.sprites_by_pos.append(next_sprite)
				self.sprites_by_link[key] = next_sprite
	
	def get_inactive_list(self):
		ret = []
		for sprite in self.sprites_by_pos:
			if not sprite.is_currently_active():
				ret.append(sprite)
		return ret
	
	def find_next_empty_node(self):
		for i, sprite in enumerate(self.sprites_by_pos):
			if sprite.is_empty():
				return i
		return len(self.sprites_by_pos)
	
	def print_output(self):
		output_table = []
		for sprite in self.sprites_by_pos:
			output_table.append(sprite.print_to_line())
		return ''.join(output_table)