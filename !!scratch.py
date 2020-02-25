from river_mwclient.esports_site import EsportsSite
import mwparserfromhell

site = EsportsSite('lol', user_file="me")  # Set wiki
summary = 'Add source'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.client.pages['Template:ContractData']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

gcd_text = '{{{{Source|gcd_after={} }}}}'
gcd_text_current = None

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
	gcd_base = 'Archive:Global_Contract_Database/NA/'
	gcd_page = None
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches('NewsData/Date'):
			y = template.get('y').value.strip()
			m = template.get('m').value.strip()
			d = template.get('d').value.strip()
			gcd_page = gcd_base + y + '-' + m + '-' + d
			gcd_text_current = gcd_text.format(gcd_page)
		if template.name.matches(['ContractData']):
			template.add('source', gcd_text_current)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
