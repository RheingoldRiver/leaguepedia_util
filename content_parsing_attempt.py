from log_into_wiki import *
import mwparserfromhell, re

site = login('me', 'lol')  # Set wiki
summary = 'Attempting to parse old content as templates'  # Set summary

page_type = 'tournament' # tournament, players, teams

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:Infobox Tournament']  # Set template
pages = this_template.embeddedin()

months = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
attrib = r'(with|from|by)'
regex = r"^\* ?" + months + r" (\d+), \[(.+?) ([^\]]*)\] ''" + attrib + r" (.+?) on (.*)''$"
no_author = r"^\* ?" + months + r" (\d+), \[(.+?) ([^\]]*)\] ''" + attrib + r" (.+?)''$"

passed_startat = False if startat_page else True
lmt = 0

def process_line(line):
	match = re.match(regex, line)
	if match:
		t = mwparserfromhell.nodes.template.Template('ContentLineOld')
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
		t = mwparserfromhell.nodes.template.Template('ContentLineOld')
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
	return None

for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat or ('2019' not in page.name and '2018' not in page.name):
		#print("Skipping page %s" % page.name)
		continue
	lmt += 1
	this_page = page
	if page_type == 'tournament':
		if site.pages[page.name + '/Media'].text() != '':
			this_page = site.pages[page.name + '/Media']
	text = this_page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches('TDRight') or template.name.matches('TabsDynamic'):
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