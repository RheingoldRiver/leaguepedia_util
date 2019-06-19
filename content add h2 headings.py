from log_into_wiki import *
import mwparserfromhell, datetime
from dateutil import parser

site = login('bot', 'lol')  # Set wiki
summary = 'Add h2 headings'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:ExternalContent/Date']  # Set template
pages = this_template.embeddedin()

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
	for template in wikitext.filter_templates():
		if template.name.matches('ExternalContent/Date'):
			m = template.get('m').value.strip()
			d = template.get('d').value.strip()
			if len(m) == 1:
				template.add('m', '0' + m)
			if len(d) == 1:
				template.add('d', '0' + d)
	text = str(wikitext)
	if '==' in text:
		continue
	lines = text.split('\n')
	for i, line in enumerate(lines):
		if 'ExternalContent/Date' in line:
			wikitext = mwparserfromhell.parse(line)
			for template in wikitext.filter_templates():
				y = template.get('y').value.strip()
				m = template.get('m').value.strip()
				d = template.get('d').value.strip()
				date_str = '{}-{}-{}'.format(y,m,d)
				date = parser.parse(date_str)
				heading = date.strftime('%b %d')
				lines[i] = '{{{{ExternalContent/End}}}}\n== {} ==\n'.format(heading) + line
	newtext = '\n'.join(lines)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)