import re, time

class TeamSpriteEntry(object):
	def __init__(self, pos, line=None):
		self.link = None
		self.pos = pos
		self.date = None
		if line:
			self.read_from_line(line)
	
	def read_from_line(self, line):
		if line != '':
			self.link = re.search(r'\["(.*)"\]', line)[0].strip()
			self.date = re.search(r'date = (\d+)', line)[0].strip()
			assert(re.search(r'pos = (\d+)', line)[0].strip() == str(self.pos))
		
	def print_to_line(self):
		if self.link and self.date:
			return '\t["{}"] = {{ pos = {}, date = {} }},\n'.format(self.link, self.pos, self.date)
		else:
			return '\n'
	
	def is_currently_active(self):
		# active will mean used in the past 24 hours
		return time.time() - int(self.date) > 60 * 60 * 24
	
	def is_empty(self):
		return not self.link
	
	def destroy(self):
		self.link = None
		self.date = None
	
	def set_active(self):
		self.date = time.time()
	
	def add_item(self, team):
		self.link = team
		self.set_active()

class SpriteSheet(object):
	def __init__(self, file):
		self.next_empty_node = None
		self.sprites_by_pos = []
		self.sprites_by_link = {}
		for i, line in enumerate(file.split('\n')):
			sprite = TeamSpriteEntry(i+1, line=line)
			self.sprites_by_pos[i] = sprite
			self.sprites_by_link[sprite.link] = sprite
			if not self.next_empty_node and sprite.is_empty():
				self.next_empty_node = i
	
	def add_activity(self, text):
		pattern = r'.*src\=\"(.+?)logo_std.png\".*'
		for team in re.search(pattern, text):
			self.sprites_by_link[team.replace('_',' ')].set_active()
	
	def check_activity(self):
		for sprite in self.sprites_by_pos:
			if not sprite.is_currently_active():
				sprite.destroy()
	
	def print_output(self):
		output_table = []
		for sprite in self.sprites_by_pos:
			output_table.append(sprite.print_to_line())
		return ''.join(output_table)
	
	def find_next_empty_node(self):
		for i, sprite in enumerate(self.sprites_by_pos):
			if sprite.is_empty():
				self.next_empty_node = i
				return
		self.next_empty_node = len(self.sprites_by_pos)