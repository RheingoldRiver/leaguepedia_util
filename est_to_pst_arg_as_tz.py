from log_into_wiki import *
from template_list import *
import mwparserfromhell, dateutil.parser, pytz

site = login('me', 'lol')  # Set wiki
summary = 'EST -> PST'  # Set summary

limit = -1
# startat_page = 'asdf'
with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages_var = [site.pages[page.strip()] for page in pages]
startat = -1

pst = pytz.timezone('America/Los_Angeles')
est = pytz.timezone('America/New_York')

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if [_ for _ in scoreboard_templates if _ == str(template.name).strip()]:
				if template.has('EST'):
					if template.get('EST').value.strip() == '':
						pass
					else:
						date = template.get("date").value.strip()
						time = template.get("EST").value.strip()
						date_time = dateutil.parser.parse(date + " " + time)
						date_time_local = est.localize(date_time)
						PST = date_time_local.astimezone(pst)
						newdate = PST.strftime('%Y-%m-%d')
						newtime = PST.strftime('%H:%M')
						template.add('PST', newtime)
						template.add('date', newdate)
					template.remove('EST')
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)