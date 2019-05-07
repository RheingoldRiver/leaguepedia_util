from log_into_wiki import *
import mwparserfromhell

site = login('me', 'gears-esports')  # Set wiki
summary = 'Fix YT'  # Set summary

limit = -1
#startat_page = 'Dirtgen'
this_template = site.pages['Template:Infobox Player']
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
			if template.name.matches('Infobox Player'):
				if template.has('youtube'):
					yt = template.get('youtube').value.strip()
					if 'youtube' in yt:
						pass
					else:
						yt = 'https://youtube.com/user/' + yt
						yt = yt.replace('user//','user/')
						template.add('youtube', yt )
				if template.has('youtube2'):
					yt = template.get('youtube2').value.strip()
					yt = 'https://youtube.com/channel/' + yt
					yt = yt.replace('channel//', 'channel/')
					template.add('youtube', yt)
					template.remove('youtube2')
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)