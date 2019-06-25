from log_into_wiki import *
import mwparserfromhell, re

site = login('me', 'lol')  # Set wiki
summary = 'Attempting to parse old content as templates'  # Set summary

page_type = 'teams' # tournament, players, teams

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'YellOwStaR'
template_by_type = {
	'players' : 'Player',
	'teams' : 'Team',
	'tournament' : 'Tournament'
}
this_template = site.pages['Template:Infobox ' + template_by_type[page_type]]  # Set template
pages = this_template.embeddedin()

months = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
date = r" (\d+)(?:st|th|rd|nd)?[.,]? ?(?:\d\d\d\d, )?"
attrib_sep = r" ?(?:\([\dms]+\) )? ?(?: *\- *)?''"
attrib = r'(with|from|by|From|By|With)'
regex = r"^\* ?" + months + date + r"\[(.+?) ([^\]]*)\]" + attrib_sep + attrib + r" (.+?) on (.*)'' *$"
no_author = r"^\* ?" + months + date + r"\[(.+?) ([^\]]*)\]" + attrib_sep + attrib + r" (.+?)'' *$"
translator = r"^\* ?" + months + date + r"\[(.+?) ([^\]]*)\]" + attrib_sep + '(translated by)' + r" (.+?) on (.*)'' *$"

passed_startat = False if startat_page else True
lmt = 0

# pages = [
# site.pages["LCK/2018_Season/Summer_Season"],
# site.pages["LCS/2019_Season/Spring_Season/Media"],
# site.pages["2015_Mid-Season_Invitational"],
# site.pages["2016_Season_World_Championship/Media"],
# site.pages["EU_LCS/2017_Season/Spring_Season"],
# site.pages["EU_LCS/2018_Season/Summer_Season/Media"],
# site.pages["LCK/2016_Season/Summer_Season"],
# site.pages["IEM_Season_IX_-_World_Championship"],
# site.pages["LCK/2019_Season/Spring_Season/Media"],
# site.pages["LLN/2018_Season/Opening_Season"],
# site.pages["2017_Season_World_Championship/Main_Event/Media"],
# site.pages["2018_Season_World_Championship/Media"],
# site.pages["LCK/2017_Season/Spring_Season"],
# site.pages["LLA/2019_Season/Opening_Season/Media"],
# site.pages["Magyar_Nemzeti_E-sport_Bajnokság/Regular_Season"]
# ]

def process_line(line):
	match = re.match(regex, line)
	if match:
		t = mwparserfromhell.nodes.template.Template('ExternalContent/Line')
		t.add('url', match[3])
		t.add('title', [match[4]])
		t.add(page_type, page.name.replace('/Media', ''))
		t.add('publication', match[7])
		t.add('author', match[6])
		if match[5] == 'with':
			t.add('type', 'interview')
		t.add('date', match[1] + ' ' + match[2])
		if 'youtube' in match[3] or 'youtu.be' in match[3]:
			t.add('isvideo', 'yes')
		lines[j] = str(t)
		return t
	match = re.match(no_author, line)
	if match:
		t = mwparserfromhell.nodes.template.Template('ExternalContent/Line')
		t.add('url', match[3])
		t.add('title', [match[4]])
		t.add(page_type, page.name.replace('/Media',''))
		t.add('publication', match[6])
		if match[5] == 'with':
			t.add('type', 'interview')
		t.add('date', match[1] + ' ' + match[2])
		if 'youtube' in match[3] or 'youtu.be' in match[3]:
			t.add('isvideo', 'yes')
		lines[j] = str(t)
		return t
	match = re.match(translator, line)
	if match:
		t = mwparserfromhell.nodes.template.Template('ExternalContent/Line')
		t.add('url', match[3])
		t.add('title', [match[4]])
		t.add(page_type, page.name.replace('/Media', ''))
		t.add('publication', match[7])
		t.add('translator', match[6])
		if match[5] == 'with':
			t.add('type', 'interview')
		t.add('date', match[1] + ' ' + match[2])
		if 'youtube' in match[3] or 'youtu.be' in match[3]:
			t.add('isvideo', 'yes')
		lines[j] = str(t)
		return t
	return None

for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat: # or ('2019' not in page.name and '2018' not in page.name):
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	this_page = page
	if page_type == 'tournament':
		if site.pages[page.name + '/Media'].text() != '':
			this_page = site.pages[page.name + '/Media']
	print('beginning page %s' % page.name)
	text = this_page.text()
	wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
	for template in wikitext.filter_templates(recursive=False):
		if tl_matches(template, ['TD','TDRight','TabsDynamic']):
			i = 1
			while template.has('content' + str(i)):
				content = template.get('content' + str(i)).value.strip()
				lines = content.split('\n')
				for j, line in enumerate(lines):
					tl = process_line(line)
					if tl:
						lines[j] = str(tl)
				template.add('content' + str(i), '\n'.join(lines))
				i+=1
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % this_page.name)
		this_page.save(newtext, summary=summary)
	else:
		pass
		#print('Skipping page %s...' % this_page.name)
