from log_into_wiki import *
import mwparserfromhell, dateutil.parser, pytz

site = login('me', 'smite-esports')  # Set wiki
summary = 'EST -> PST'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:GameSchedule5'] # Set template
pages = this_template.embeddedin()
startat = -1

pst = pytz.timezone('America/Los_Angeles')
est = pytz.timezone('America/New_York')

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('GameSchedule5'):
				if template.has('timezone') and template.has('time'):
					if template.get('timezone').value.strip() == 'EST':
						date = template.get("date").value.strip()
						time = template.get("time").value.strip()
						date_time = dateutil.parser.parse(date + " " + time)
						date_time_local = est.localize(date_time)
						PST = date_time_local.astimezone(pst)
						newdate = PST.strftime('%Y-%m-%d')
						newtime = PST.strftime('%H:%M')
						template.add('timezone','PST')
						template.add('time',newtime)
						template.add('date',newdate)
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)
