from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell, datetime
from dateutil import parser

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Attempting to migrate content to data ns'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.client.pages['Template:ExternalContent/Line']  # Set template
pages = this_template.embeddedin()

tabs_templates = ['TDRight', 'TabsDynamic', 'TD']
years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']

pages = [
site.client.pages["User:RheingoldRiver/content/2015"],
]

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
	for y in years:
		if y in page.name:
			year = y
			break
	if not year:
		continue
	print('Beginning page %s' % page.name)
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates(recursive=False):
		print(template.name)
		if template.name.matches(tabs_templates):
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
						if param_tl.has('date'):
							this_year = section_year
							if param_tl.has('year'):
								this_year = param_tl.get('year').value.strip()
							date_str = param_tl.get('date').value.strip() + ', ' + this_year
							print(date_str)
							date = parser.parse(date_str)
							idx = (date.weekday() + 1) % 7
							sun = date - datetime.timedelta(idx)
							data_page_name = 'Data:ExternalContent/' + sun.strftime('%Y-%m-%d')
							print(data_page_name)
							data_page = site.client.pages[data_page_name]
							data_text = data_page.text()
							if param_tl.has('url') and param_tl.get('url').value.strip() in data_text:
								param_tl.add('finished', 'yes')
								continue
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
				template.add('content' + str(i), str(param_wikitext))
				i = i + 1
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
