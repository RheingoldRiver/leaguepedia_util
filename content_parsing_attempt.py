from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell, re

site = EsportsClient('lol', user_file="bot") # Set wiki
summary = 'Attempting to parse old content as templates'  # Set summary

page_type = 'players' # tournament, players, teams

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'YellOwStaR'
template_by_type = {
	'players' : 'Player',
	'teams' : 'Team',
	'tournament' : 'Tournament'
}
this_template = site.client.pages['Template:Infobox ' + template_by_type[page_type]]  # Set template
pages = this_template.embeddedin()

months = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?'
date = r" *(\d+)(?:st|th|rd|nd)?[.,]? ?(?:\d\d\d\d,? ?)?(?: *\- *)?"
attrib_sep = r" ?(?:\([\dms]+\) )? ?(?: *\- *)?''"
attrib = r'(?: *\- *)?(with|from|by|From|By|With)'
regex = r"^\* ?" + months + date + r"\[(.+?) ([^\]]*)\]" + attrib_sep + attrib + r" (.+?) on (.*)'' *$"
no_author = r"^\* ?" + months + date + r"\[(.+?) ([^\]]*)\]" + attrib_sep + attrib + r" (.+?)'' *$"
translator = r"^\* ?" + months + date + r"\[(.+?) ([^\]]*)\]" + attrib_sep + '(translated by)' + r" (.+?) on (.*)'' *$"

passed_startat = False if startat_page else True
lmt = 0

pages = site.client.pages['Template:ExternalContent/Line'].embeddedin(namespace=0)

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
		if site.client.pages[page.name + '/Media'].text() != '':
			this_page = site.client.pages[page.name + '/Media']
	print('beginning page %s' % page.name)
	text = this_page.text()
	wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
	is_right_type = False
	for template in wikitext.filter_templates(recursive=False):
		if template.name.matches('Infobox ' + template_by_type[page_type]):
			is_right_type = True
		if template.name.matches(['TD','TDRight','TabsDynamic', 'TDR']) and is_right_type:
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
