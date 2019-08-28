from esports_site import EsportsSite
from datetime import date, timedelta
import mwparserfromhell

site = EsportsSite('bot', 'lol')  # Set wiki
template_prefix = 'NewsData'
data_prefix = 'News'
navbox_template = 'NewsData'
summary = 'Initializing %s Pages' % template_prefix # Set summary

def allsundays(year):
	d = date(year, 1, 1)						  # January 1st
	d += timedelta(days = 6 - d.weekday())  # First Sunday
	while d.year == year:
		yield d
		d += timedelta(days = 7)

for year in range(2009,2020):
	site.pages['Data:{}/{}'.format(data_prefix, year)].save('{{NewsDataOverview}}', summary=summary)
	year_switch = '|' + str(year) + '='
	list_of_sundays = [year_switch]
	for d in allsundays(year):
		list_of_sundays.append('* [[Data:{}/{}|{}]]'.format(data_prefix, d.strftime('%Y-%m-%d'), str(d.strftime('%b %d'))))
		
		# START SAVING DATA PAGES - COMMENT THIS BLOCK TO DO NAVBOX ONLY
		p = site.pages['Data:{}/{}'.format(data_prefix, str(d))]
		if p.text() != '':
			continue
		lines = [ '{{%s/Start}}' % template_prefix ]
		weekday_index = d
		for i in range(0,7):
			y = weekday_index.year
			m = '{:02d}'.format(weekday_index.month)
			day = '{:02d}'.format(weekday_index.day)
			lines.append('== {} =='.format(weekday_index.strftime('%b %d')))
			lines.append('{{{{{}/Date|y={}|m={}|d={}}}}}'.format(template_prefix, y, m, day))
			weekday_index += timedelta(days = 1)
			lines.append('{{%s/End}}' % template_prefix)
		p.save('\n'.join(lines), summary=summary)
		# END SAVING DATA PAGES - COMMENT THIS BLOCK TO DO NAVBOX ONLY
	
	list_of_sundays.append('}}\n{{Endflatlist}}')
	template_page = site.pages['Template:%s Navbox' % navbox_template]
	wikitext = mwparserfromhell.parse(template_page.text())
	for template in wikitext.filter_templates():
		if template.name.matches('Navbox'):
			text = str(template.get('list1').value)
			if year_switch in text:
				break
			text = text.replace('{{Endflatlist}}',
								'* [[Data:{}/{}|{}]]\n{{{{Endflatlist}}}}'.format(data_prefix, str(year), str(year)))
			template.add('list1', text)
			list_text = template.get('list2').value
			list_text = list_text.replace('}}\n{{Endflatlist}}', '\n'.join(list_of_sundays))
	template_page.save(str(wikitext))
