from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell, datetime
import re
from dateutil import parser

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Attempting to migrate content to data ns'  # Set summary

page_type = 'players' # players or teams

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'Nukeduck'
template_types = {
	"players" : 'Player',
	"teams" : 'Team'
}
this_template = site.client.pages['Template:Infobox ' + template_types[page_type]]  # Set template
pages = this_template.embeddedin()

tabs_templates = ['TDRight', 'TabsDynamic', 'TD']
years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']

# pages = [
# site.client.pages["Wraith"]
# ]

pages = site.client.pages['Template:ExternalContent/Line'].embeddedin(namespace=0)

def add_player_to_line(data_tl, name):
	if not data_tl.has(page_type):
		data_tl.add(page_type, page.name)
		return
	r = r'(^|,)' + re.escape(name) + r'($|,)'
	if re.search(r, data_tl.get(page_type).value.strip()):
		return
	page_type_val = data_tl.get(page_type).value.strip()
	data_tl.add(page_type, page_type_val + ',' + page.name)

def add_new_line(param_tl, data_page, data_text, date):
	sep = '{{{{ExternalContent/Date|y={}|m={}|d={}}}}}\n'.format(
		date.year,
		date.strftime('%m'),
		date.strftime('%d')
	)
	print(sep)
	data_text_tbl = data_text.split(sep)
	data_text_new = data_text_tbl[0] + sep + str(param_tl) + '\n' + data_text_tbl[1]
	data_page.save(data_text_new, summary=summary)
	param_tl.add('finished', 'yes')

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
	is_right_type = False
	for template in wikitext.filter_templates(recursive=False):
		if template.name.matches('Infobox ' + template_types[page_type]):
			is_right_type = True
		if template.name.matches(tabs_templates) and is_right_type:
			i = 1
			while template.has('name' + str(i)) and template.has('content' + str(i)):
				param_text = template.get('content' + str(i)).value.strip()
				param_wikitext = mwparserfromhell.parse(param_text)
				section_year = year
				section_name = template.get('name' + str(i)).value.strip()
				for y in years:
					if y in section_name:
						section_year = y
						break
				for param_tl in param_wikitext.filter_templates():
					if not section_year:
						continue
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
							data_page = site.client.pages[data_page_name]
							data_text = data_page.text()
							if param_tl.get('url').value.strip() not in data_text:
								add_new_line(param_tl, data_page, data_text, date)
							else:
								data_wikitext = mwparserfromhell.parse(data_text)
								for data_tl in data_wikitext.filter_templates():
									if not data_tl.has('url'):
										continue
									if data_tl.get('url').value.strip() != url:
										continue
									in_data_page = True
									print(data_page_name)
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
