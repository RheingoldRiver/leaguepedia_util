import re, threading, mwparserfromhell
from log_into_wiki import *

#################################################################################################

original_name = 'Duke'
irl_name = "Lee Ho-seong"
new_name = '{} ({})'.format(original_name, irl_name.strip())
init_move = True
blank_edit = False
limit = -1
timeout_limit = 30

listplayer_templates = ["listplayer", "listplayer/Current"]
roster_templates = ["ExtendedRosterLine", "ExtendedRosterLine/MultipleRoles"]
scoreboard_templates = ["MatchRecapS8/Player","Scoreboard/Player"]
stat_templates = ["IPS", "CareerPlayerStats", "MatchHistoryPlayer"]
player_line_templates = ["LCKPlayerLine", "LCSPlayerLine"]
roster_change_templates = ["RosterChangeLine", "RosterRumorLine2",
						   "RosterRumorLineStay", "RosterRumorLineNot", "RosterRumorLine"]
summary = "Disambiguating {} to {}".format(original_name, new_name)

css_style = " {\n    color:orange!important;\n    font-weight:bold;\n}"

orig_name_lc = original_name[0].lower() + original_name[1:]
new_name_lc = new_name[0].lower() + new_name[1:]

blank_edit_these = []

#############################################################################################

def savepage(targetpage, savetext):
	targetpage.save(savetext, summary=summary, tags="bot_disambig")

def blank_edit_page(page):
	textname = str(page.name)
	newpage = site.pages[textname]
	text = newpage.text(cache=False)
	page.save(text, summary="Blank Editing")

def move_page(from_page):
	new_page_name = str(from_page.name).replace(original_name, new_name)
	new_page = site.pages[new_page_name]
	if new_page.exists:
		print("{} already exists, cannot move!".format(from_page.name))
	else:
		print("Moving page {} to {}".format(from_page.name, new_page_name))
		from_page.move(new_page_name, reason=summary, no_redirect=True)
		blank_edit_these.append(new_page)

def edit_concept(concept):
	text = concept.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches("PlayerGamesConcept"):
			i = 1
			while template.has(i):
				if template.get(i).strip() == original_name:
					template.add(i, new_name)
				elif template.get(i).strip() == orig_name_lc:
					template.add(i, new_name_lc)
				i = i + 1
	newtext = str(wikitext)
	if newtext != text:
		concept.save(newtext, summary=summary, tags="bot_disambig")

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

def process_page(page):
	print("Processing next page: " + page.name)
	text = page.text()
	origtext = text
	# do links first because it's easier to just edit them as a string
	if text.lower().startswith('#redirect') and page.name.lower() == original_name.lower():
		pass
	else:
		text = text.replace("[[" + original_name + "]]", "[[" + new_name + "|" + original_name + "]]")
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		process_template(template)
	newtext = str(wikitext)
	if origtext != newtext or blank_edit:
		print("Saving...")
		t = threading.Thread(target=savepage, kwargs={"targetpage": page, "savetext": newtext})
		t.start()
		t.join(timeout=timeout_limit)
	else:
		print("No changes, skipping")

def check_list(template, param, sep = ','):
	if not template.has(param):
		return
	text_initial = template.get(param).value.strip()
	tbl = text_initial.split(sep)
	made_changes = False
	for i, val in enumerate(tbl):
		if val.strip() == original_name:
			made_changes = True
			tbl[i] = new_name
	if made_changes:
		template.add(param, sep.join(tbl))


def process_template(template):
	def tl_matches(arr, field=None):
		if field:
			has_field = False
			if template.has(field):
				has_field = template.get(field).value.strip() == original_name
			return [_ for _ in arr if template.name.matches(_)] and has_field
		return [_ for _ in arr if template.name.matches(_)]
	
	if tl_matches(['bl'], field=1) and not template.has(2):
		template.add(1, new_name)
		template.add(2, original_name)

	elif tl_matches(listplayer_templates, field=1) and not template.has("link"):
		template.add("link", new_name, before=1)
	
	elif tl_matches(roster_templates, field='player') and not template.has('link'):
		template.add("link", new_name, before="name")
	
	elif tl_matches(scoreboard_templates, field='name'):
		template.add("link", new_name, before="kills")
	
	elif tl_matches(roster_change_templates, field='player'):
		template.add("player", new_name + "{{!}}" + original_name)
	
	elif tl_matches(['TeamRoster/Line', 'RosterLineOld'], field='player'):
		template.add('link', new_name)
	
	elif tl_matches(player_line_templates, field=1):
		template.add(2, new_name)
	
	elif tl_matches(['Player', 'RSRR/Player'], field=1):
		template.add('link', new_name)
	
	elif tl_matches(["MatchDetails/Series"], field='mvp'):
		template.add("mvplink", new_name, before="mvp")
	
	elif tl_matches(["PentakillLine"], field=6):
		template.add("playerlink", new_name, before=6)
	
	elif tl_matches(["MatchSchedule","MatchSchedule/Game"]):
		if template.has("mvp"):
			if template.get("mvp").value.strip() == original_name:
				template.add("mvp", new_name)
		check_list(template, 'with')
		check_list(template, 'pbp')
		check_list(template, 'color')
	
	elif tl_matches(['ExternalContent/Line']):
		check_list(template, 'players')
	
	elif tl_matches(['SeasonAward']):
		if template.has(1):
			if template.get(1).value.strip() == original_name:
				template.add('link', new_name)
		check_links(template, 'eligibleplayers', 'eligiblelinks', ',', original_name, new_name)
	
	elif tl_matches(['PlayerImageMetadata'], field="playerlink"):
		template.add('playerlink', new_name)
	
	elif tl_matches(['RCPlayer'], field="player"):
		template.add('playerlink', new_name)

	elif tl_matches(["PortalCurrentRosters"]):
		for pos in ['t', 'j', 'm', 'a', 's']:
			for period in ['old', 'new']:
				arg_name = pos + '_' + period
				arg_link = arg_name + '_links'
				check_links(template, arg_name, arg_link, ',', original_name, new_name)

def make_disambig_page():
	text = "{{DisambigPage\n|player1=" + new_name + "\n|player2=\n}}"
	page = site.pages[original_name]
	old_text = page.text()
	if 'disambigpage' not in old_text.lower():
		page.save(text, summary=summary)

site = login('me','lol')

thispage = site.pages[original_name]
newpage = site.pages[new_name]

if init_move:
	move_page(thispage)
	subpages = site.allpages(prefix=original_name + "/")
	for subpage in subpages:
		edit_subpage(subpage)
		move_page(subpage)
	concept = site.pages["Concept:{}/Games".format(original_name)]
	if concept.exists:
		edit_concept(concept)
		move_page(concept)


pages = thispage.backlinks()
i = 0
for page in pages:
	if i == limit:
		break
	i = i + 1
	process_page(page)
print("Blank editing...")
if init_move:
	for page in blank_edit_these:
		blank_edit_page(page)
	make_disambig_page()
print("Done! If some pages stalled out you may still need to abort manually.")
