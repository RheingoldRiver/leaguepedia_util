from log_into_wiki import *
from datetime import date, timedelta

site = login('bot', 'lol')  # Set wiki
summary = 'Initializing Content Pages'  # Set summary

def allsundays(year):
	d = date(year, 1, 1)						  # January 1st
	d += timedelta(days = 6 - d.weekday())  # First Sunday
	while d.year == year:
		yield d
		d += timedelta(days = 7)

for y in [2011, 2012, 2014, 2015, 2016, 2017, 2018, 2019]:
	for d in allsundays(y):
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