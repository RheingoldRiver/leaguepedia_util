import re, threading, mwparserfromhell
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

#################################################################################################

original_name = 'Ali'
irl_name = "Liu Xu-Dong"
new_name = '{} ({})'.format(original_name, irl_name.strip())
init_move = True
limit = -1
timeout_limit = 30

scoreboard_templates = ["MatchRecapS8/Player","Scoreboard/Player"]
stat_templates = ["CareerPlayerStats", "MatchHistoryPlayer"]
roster_change_templates = ["RosterChangeLine", "RosterRumorLine2",
						   "RosterRumorLineStay", "RosterRumorLineNot", "RosterRumorLine"]
summary = "Disambiguating {} to {}".format(original_name, new_name)

orig_name_lc = original_name[0].lower() + original_name[1:]
new_name_lc = new_name[0].lower() + new_name[1:]
orig_name_uc = original_name[0].upper() + original_name[1:]
new_name_uc = new_name[0].upper() + new_name[1:]

blank_edit_these = []

#############################################################################################

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki

def savepage(targetpage, savetext):
	targetpage.save(savetext, summary=summary, tags="bot_disambig")

def move_page(from_page):
	new_page_name = str(from_page.name).replace(orig_name_uc, new_name)
	new_page = site.client.pages[new_page_name]
	if new_page.exists:
		print("{} already exists, cannot move!".format(from_page.name))
	else:
		print("Moving page {} to {}".format(from_page.name, new_page_name))
		from_page.move(new_page_name, reason=summary, no_redirect=True)
		blank_edit_these.append(new_page)

def edit_subpage(subpage):
	text = subpage.text()
	wikitext = mwparserfromhell.parse(text)
	for stemplate in wikitext.filter_templates():
		if stemplate.has(1):
			if stemplate.get(1).value.strip() == original_name:
				stemplate.add(1, new_name)
	newtext = str(wikitext)
	if text != newtext:
		print("Editing " + subpage.name + "...")
		subpage.save(newtext, reason=summary)


class PageProcessor(object):
	def __init__(self, this_orig, this_new):
		self.original_name = this_orig
		self.new_name = this_new
	
	def run(self, page):
		print("Processing next page: " + page.name)
		text = page.text()
		origtext = text
		# do links first because it's easier to just edit them as a string
		if text.lower().startswith('#redirect') and page.name.lower() == self.original_name.lower():
			pass
		else:
			text = text.replace("[[" + self.original_name + "]]", "[[" + self.new_name + "|" + self.original_name + "]]")
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			self.process_template(template)
		newtext = str(wikitext)
		if origtext != newtext:
			print("Saving...")
			t = threading.Thread(target=savepage, kwargs={"targetpage": page, "savetext": newtext})
			t.start()
			t.join(timeout=timeout_limit)
		else:
			print("No changes, skipping")
	
	def check_list(self, template, param, sep = ','):
		if not template.has(param):
			return
		text_initial = template.get(param).value.strip()
		tbl = text_initial.split(sep)
		made_changes = False
		for i, val in enumerate(tbl):
			if val.strip() == self.original_name:
				made_changes = True
				tbl[i] = self.new_name
		if made_changes:
			template.add(param, sep.join(tbl))
	
	@staticmethod
	def parse_ordered_field(val, sep):
		if not sep:
			sep = ','
		tbl = re.split('\s*' + sep + '\s*' + '\s*', val)
		return tbl
	
	def check_links(self, template, key1, key2, sep, name, link):
		if not sep:
			sep = ','
		if template.has(key1):
			val1 = template.get(key1).value.strip()
			tbl1 = self.parse_ordered_field(val1, sep)
			tbl2 = ['' for _ in range(len(tbl1))] # list(range(len(tbl1)))
			if template.has(key2):
				val2 = template.get(key2).value.strip()
				tbl2 = self.parse_ordered_field(val2, sep)
			if name in tbl1:
				i = tbl1.index(name)
				tbl2[i] = link
				template.add(key2,sep.join(tbl2), before=key1)
				template.add(key1, val1, before=key2)
	
	def process_template(self, template):
		def tl_matches(arr, field=None):
			if field:
				has_field = False
				if template.has(field):
					has_field = template.get(field).value.strip() == self.original_name
				return [_ for _ in arr if template.name.matches(_)] and has_field
			return [_ for _ in arr if template.name.matches(_)]
		
		if tl_matches(['bl'], field=1) and not template.has(2):
			template.add(1, self.new_name)
			template.add(2, self.original_name)
		
		elif tl_matches(["listplayer", "listplayer/Current"], field=1):
			if not template.has("link"):
				template.add(1, self.new_name)
		
		elif tl_matches(scoreboard_templates, field='link'):
			template.add("link", self.new_name)
		
		elif tl_matches(roster_change_templates, field='player'):
			template.add("player", self.new_name + "{{!}}" + self.original_name)
		
		elif tl_matches(
				['TeamRoster/Line', 'RosterLineOld', 'ExtendedRosterLine', 'ResidencyChange'],
				field='player'
		):
			template.add('player', self.new_name)
		
		elif tl_matches(['Player', 'RSRR/Player'], field=1):
			template.add('link', self.new_name)
		
		elif tl_matches(["MatchDetails/Series"], field='mvp'):
			template.add("mvplink", self.new_name, before="mvp")
		
		elif tl_matches(["PentakillLine"], field=6):
			template.add("playerlink", self.new_name, before=6)
		
		elif tl_matches(["MatchSchedule","MatchSchedule/Game"]):
			if template.has("mvp"):
				if template.get("mvp").value.strip() == self.original_name:
					template.add("mvp", self.new_name)
			self.check_list(template, 'with')
			self.check_list(template, 'pbp')
			self.check_list(template, 'color')
		
		elif tl_matches(['ExternalContent/Line']):
			self.check_list(template, 'players')
		
		elif tl_matches(['SeasonAward']):
			if template.has(1):
				if template.get(1).value.strip() == self.original_name:
					template.add('link', self.new_name)
			self.check_links(template, 'eligibleplayers', 'eligiblelinks', ',', self.original_name, self.new_name)
		
		elif tl_matches(['PlayerImageMetadata'], field="playerlink"):
			template.add('playerlink', self.new_name)
		
		elif tl_matches(['RCPlayer', 'PlayerPronunciationFile'], field="player"):
			template.add('player', self.new_name)
		
		elif tl_matches(['PlayerRename'], field="original"):
			template.add('original', self.new_name)
		
		elif tl_matches(['PlayerRename'], field="new"):
			template.add('new', self.new_name)
		
		elif tl_matches(["PortalCurrentRosters"]):
			for pos in ['t', 'j', 'm', 'a', 's']:
				for period in ['old', 'new']:
					arg_name = pos + '_' + period
					arg_link = arg_name + '_links'
					self.check_links(template, arg_name, arg_link, ',', self.original_name, self.new_name)

def make_disambig_page():
	text = "{{DisambigPage\n|player1=" + new_name + "\n|player2=\n}}"
	page = site.client.pages[original_name]
	old_text = page.text()
	if 'disambigpage' not in old_text.lower():
		page.save(text, summary=summary)

thispage = site.client.pages[original_name]

if init_move:
	move_page(thispage)
	subpages = site.client.allpages(prefix=original_name + "/")
	for subpage in subpages:
		edit_subpage(subpage)
		move_page(subpage)
	tooltip_page = site.client.pages['Tooltip:' + original_name]
	move_page(tooltip_page)

pages = thispage.backlinks()
i = 0

# fix cases of both first letter lowercase and first letter uppercase
processor_lc = PageProcessor(orig_name_lc, new_name_lc)
processor_uc = PageProcessor(orig_name_uc, new_name_uc)
for page in pages:
	if i == limit:
		break
	i = i + 1
	processor_lc.run(page)
	processor_uc.run(page)
print("Blank editing...")
if init_move:
	for page in blank_edit_these:
		page.touch()
	make_disambig_page()
print("Done! If some pages stalled out you may still need to abort manually.")
