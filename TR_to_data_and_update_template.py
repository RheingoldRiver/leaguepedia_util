from log_into_wiki import *
import mwparserfromhell

site = login('me', 'fortnite-esports')  # Set wiki
summary = 'TR to data and update template'  # Set summary

limit = -10
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:TournamentResultsLineDuos']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

# pages = [site.pages['Fortnite World Cup 2019/South America/Week 3']]

def parse_text(s):
	tbl = s.split('\n')
	ret = ['{{DataTabs}}']
	for line in tbl:
		new_line = None
		if 'TournamentResultsStart' in line:
			new_line = line.replace('}}','')
			new_line = new_line.replace('TournamentResultsStart','TournamentResults')
		elif '{{TournamentResultsLine' in line:
			new_line = re.sub(r'{{\w+', '|{{TournamentResults/Line', line)
		elif '{{TournamentResultsEnd' in line:
			new_line = line.replace('{{TournamentResultsEnd', '')
		if new_line:
			ret.append(new_line)
	return '\n'.join(ret)

def fix_rosters(text):
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['TournamentResults/Line']):
			if template.has('player1'):
				player = template.get('player').value.strip()
				player1 = template.get('player1').value.strip()
				template.remove('player')
				template.remove('player1')
				template.add('players', player + ',' + player1)
			elif template.has('player'):
				player = template.get('player').value.strip()
				template.remove('player')
				template.add('players', player)
	return str(wikitext)

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
	if 'TournamentResultsQuery' in text:
		continue
	print('Starting to process page %s....' % page.name)
	wikitext = mwparserfromhell.parse(text)
	for section in wikitext.get_sections(flat=True):
		old_text = str(section)
		if str(section.filter()[0].title).strip() != 'Prize Pool':
			continue
		print('Saving data page....')
		new_text = parse_text(old_text)
		new_text = fix_rosters(new_text)
		site.pages['Data:' + page.name].save(new_text, summary=summary)
		wikitext.replace(section, '{{TournamentResultsQuery}}\n')
	
	newtext = str(wikitext).replace('{{TournamentResultsQuery}}', '=== Prize Pool ===\n{{TournamentResultsQuery}}')
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
		page.save(newtext, summary='Blank editing...')
		data_page = site.pages['Data:' + page.name]
		data_page.save(data_page.text(), summary='Blank editing...')
	else:
		print('Skipping page %s...' % page.name)
