from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'birthdays with month name now'  # Set summary

limit = -1
startat_page = 'CDD'
this_template = site.pages['Template:Infobox Staff']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

lookup_month = {
	'01' : 'January',
	'02' : 'February',
	'03' : 'March',
	'04' : 'April',
	'05' : 'May',
	'06' : 'June',
	'07' : 'July',
	'08' : 'August',
	'09' : 'September',
	'10' : 'October',
	'11' : 'November',
	'12' : 'December',
	'1': 'January',
	'2': 'February',
	'3': 'March',
	'4': 'April',
	'5': 'May',
	'6': 'June',
	'7': 'July',
	'8': 'August',
	'9': 'September'
}

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
		failed = False
		for template in wikitext.filter_templates():
			if template.name.matches('Infobox Staff'):
				if template.has('birth_date_month'):
					m = template.get('birth_date_month').value.strip()
					if m in lookup_month:
						template.add('birth_date_month', lookup_month[m])
					else:
						failed = True
		newtext = str(wikitext)
		if failed:
			newtext = newtext + '[[Category:Pages with unknown birth months]]'
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)