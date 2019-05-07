from log_into_wiki import *
import re, time

site = login('bot', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
#startat_page = 'File:Hallucinate.png'
with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages = [page.strip() for page in pages]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

lmt = 0
for p in pages:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % p)
	else:
		try:
			page = site.pages[p]
			text = page.text()
			newtext = re.sub(r'Ability[ _]icons', 'Ability Icons', text)
			
			if text != newtext:
				print('Saving page %s...' % page.name)
				page.save(newtext, summary=summary)
			else:
				print('Skipping page %s...' % page.name)
		except Exception as e:
			time.sleep(10)
			site = login('bot', 'lol')
			page = site.pages[p]
			text = page.text()
			newtext = re.sub(r'Ability[ _]icons', 'Ability Icons', text)
			
			if text != newtext:
				print('Saving page %s...' % page.name)
				page.save(newtext, summary=summary)
			else:
				print('Skipping page %s...' % page.name)