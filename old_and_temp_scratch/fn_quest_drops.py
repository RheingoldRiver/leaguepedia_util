from log_into_wiki import *
import mwparserfromhell

site = login('me', 'fortnite')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
startat_page = 'Challenge the Horde 25'
this_template = site.pages['Template:Infobox Quests']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
print(startat)

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
			if template.name.matches('Infobox Quests'):
				i = 1
				j = 1
				while template.has('r' + str(i)):
					s = str(i)
					drop = template.get('r' + s).value.strip()
					amt = template.get('r' + s + 'a').value.strip() if template.has('r' + s + 'a') else ''
					template.add('reward' + str(j), '{{Reward|' + drop + '|' + amt + '}}' )
					template.remove('r' + s)
					if template.has('r' + s + 'a'):
						template.remove('r' + s + 'a')
					i += 1
					j += 1
				i = 1
				or_tbl = []
				or_tbl_amt = []
				has_or = False
				while template.has('or' + str(i)):
					has_or = True
					s = str(i)
					or_tbl.append(template.get('or' + s).value.strip())
					or_tbl_amt.append(template.get('or' + s + 'a').value.strip() if template.has('or' + s + 'a') else '' )
					template.remove('or' + s)
					if template.has('or' + s + 'a'):
						template.remove('or' + s + 'a')
					i += 1
				if has_or:
					or_tbl_output = ['{{{{Reward|{}|{}}}}}'.format(or_tbl[k], or_tbl_amt[k]) for k in range(len(or_tbl))]
					template.add('reward' + str(j),','.join(or_tbl_output))
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)