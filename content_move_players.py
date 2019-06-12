from log_into_wiki import *
import mwparserfromhell, datetime
from dateutil import parser

site = login('me', 'lol')  # Set wiki
summary = 'Attempting to migrate content to data ns'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:ExternalContent/Line']  # Set template
pages = this_template.embeddedin()

tabs_templates = ['TDRight', 'TabsDynamic', 'TD']
years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']

pages = [site.pages['Froggen']]

def add_player_to_line(data_tl, name):
	if not data_tl.has('players'):
		data_tl.add('players', page.name)
		return
	r = r'(^|,)' + re.escape(name) + r'($|,)'
	if re.search(r, data_tl.get('players').value.strip()):
		print('skipping template: ' + str(data_tl))
		return
	players = data_tl.get('players').value.strip()
	data_tl.add('players', players + ',' + page.name)
	

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if page.name.startswith('Data:'):
		continue
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	year = None
	print('Beginning page %s' % page.name)
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates(recursive=False):
		if tl_matches(template, tabs_templates):
			i = 1
			while template.has('name' + str(i)) and template.has('content' + str(i)):
				param_text = template.get('content' + str(i)).value.strip()
				param_wikitext = mwparserfromhell.parse(param_text)
				section_year = year
				section_name = template.get('name' + str(i)).value.strip()
				if section_name in years:
					section_year = section_name
				for param_tl in param_wikitext.filter_templates():
					if param_tl.name.matches('ExternalContent/Line'):
						if param_tl.has('finished') and param_tl.get('finished').value.strip() == 'yes':
							continue
						if not param_tl.has('url'):
							continue
						url = param_tl.get('url').value.strip()
						if param_tl.has('date'):
							this_year = section_year
							if param_tl.has('year'):
								this_year = param_tl.get('year').value.strip()
							date_str = param_tl.get('date').value.strip() + ', ' + this_year
							date = parser.parse(date_str)
							idx = (date.weekday() + 1) % 7
							sun = date - datetime.timedelta(idx)
							data_page_name = 'Data:ExternalContent/' + sun.strftime('%Y-%m-%d')
							print(data_page_name)
							data_page = site.pages[data_page_name]
							data_text = data_page.text()
							if param_tl.get('url').value.strip() not in data_text:
								continue
							data_wikitext = mwparserfromhell.parse(data_text)
							for data_tl in data_wikitext.filter_templates():
								if not data_tl.has('url'):
									continue
								if data_tl.get('url').value.strip() != url:
									continue
								print('url found')
								add_player_to_line(data_tl, page.name)
							data_page.save(str(data_wikitext), summary = summary)
							param_tl.add('finished', 'yes')
				template.add('content' + str(i), str(param_wikitext))
				i = i + 1
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)