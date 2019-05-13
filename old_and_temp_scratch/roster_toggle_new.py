from log_into_wiki import *
import mwparserfromhell

site = login('bot','lol') # Set wiki
summary = 'Replace TeamRoster/Button with new' # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'ESL Benelux 5on5 Opening Cup'
this_template = site.pages['Template:TeamRoster/Button'] # Set template
pages = this_template.embeddedin()

MAX_TEAMS = {
	'400' : '2',
	'600' : '3',
	'700' : '4',
	'800' : '4',
	'900' : '5',
	'1000' : '5',
	'1100' : '6',
	'1200' : '7'
}

def get_width(str):
	match = re.search(r'(\d*)px', str)
	if match:
		return match[1]
	return ''

def get_new_line(page_name, max_teams):
	roster_page = ''
	text = site.pages[page_name + '/Team Rosters'].text()
	if text != '':
		roster_page = '|showrosterpage=yes'
	return '{{{{RostersStart\n|maxteams={}{}\n}}}}'.format(max_teams, roster_page)

missing_widths = []

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for section in wikitext.get_sections(flat = True):
		section_text = section.strip()
		has_rosters = False
		section_wikitext = mwparserfromhell.parse(section_text)
		for template in section_wikitext.filter_templates():
			if template.name.matches('TeamRoster'):
				has_rosters = True
		if not has_rosters:
			continue
		lines = section_text.split('\n')
		if len(lines) > 2 and '{{TeamRoster/Button}}' in lines[1]:
			if 'match-by-match' in lines[2]:
				lines.pop(2)
			if lines[-1].endswith('</div>'):
				lines[-1] = lines[-1].replace('</div>', '')
				lines.append('{{RostersEnd}}')
			elif section_text.count('</div>') == 1:
				for i, line in enumerate(lines):
					if '</div>' in line:
						lines[i] = line.replace('</div>', '{{RostersEnd}}')
			else:
				continue
			lines.pop(1)
			width = get_width(lines[1])
			print(width + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			if width in MAX_TEAMS:
				lines[1] = get_new_line(page.name, MAX_TEAMS[width])
				wikitext.replace(section, '\n'.join(lines) + '\n')
			else:
				missing_widths.append(width)
			
		elif len(lines) > 2 and '{{TeamRoster/Button}}' in lines[1] and '|start}}' in lines[2]:
			lines[1] = '{{RostersStart}}'
			lines.append('{{RostersEnd}}')
			wikitext.replace(section, '\n'.join(lines) + '\n')
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
		
print(missing_widths)