from log_into_wiki import *
from datetime import date, timedelta
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Initializing Content Pages'  # Set summary

def allsundays(year):
	d = date(year, 1, 1)						  # January 1st
	d += timedelta(days = 6 - d.weekday())  # First Sunday
	while d.year == year:
		yield d
		d += timedelta(days = 7)

for y in [2020]:
	list_of_sundays = ['|' + str(y) + '=']
	for d in allsundays(y):
		list_of_sundays.append('* [[Data:ExternalContent/{}|{}]]'.format(d.strftime('%Y-%m-%d'), str(d.strftime('%b %d'))))
		p = site.pages['Data:ExternalContent/' + str(d)]
		if p.text() != '':
			continue
		lines = [ '{{ExternalContent/Start}}' ]
		weekday_index = d
		for i in range(0,7):
			y = weekday_index.year
			m = weekday_index.month
			day = weekday_index.day
			lines.append('{{{{ExternalContent/Date|y={}|m={}|d={}}}}}'.format(y, m, day))
			weekday_index += timedelta(days = 1)
		lines.append('{{ExternalContent/End}}')
		print('\n'.join(lines))
		p.save('\n'.join(lines), summary=summary)
	list_of_sundays.append('}}\n{{Endflatlist}}')
	template_page = site.pages['Template:External Content Navbox']
	wikitext = mwparserfromhell.parse(template_page.text())
	for template in wikitext.filter_templates():
		if template.name.matches('Navbox'):
			text = str(template.get('list1').value)
			text = text.replace('{{Endflatlist}}',
								'* [[Data:ExternalContent/{}|{}]]\n{{{{Endflatlist}}}}'.format(str(y), str(y)))
			template.add('list1', text)
			list_text = template.get('list2').value
			list_text = list_text.replace('}}\n{{Endflatlist}}', '\n'.join(list_of_sundays))
	template_page.save(str(wikitext))