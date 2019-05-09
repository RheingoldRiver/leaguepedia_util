from log_into_wiki import *
import mwparserfromhell

site = login('bot','lol') # Set wiki
summary = 'Converting streams to use stream template' # Set summary

limit = -1
startat_page = 'Copenhagen Games 2014'
this_template = site.pages['Template:Infobox Tournament'] # Set template
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

STREAM_NAMES = ['Twitch', 'YouTube', 'Azubu', 'Hitbox', 'Afreeca', 'Douyu', 'Twitch.tv'
				'CubeTV', 'Mobcrush', 'Youtube Gaming', 'OPENREC', 'Facebook Gaming', 'NimoTV', 'Naver']

re_find = r'\{\{flag\|\s*(\w+)\s*\}\}\s*\[([^\s]*) (.+?)\]'
re_repl_no_display = r'{{stream|url=\2|lang=\1}}'
re_repl_display = r'{{stream|url=\2|lang=\1|display=\3}}'

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
		print(page.name)
		for section in wikitext.get_sections():
			if section.filter_headings() and section.filter_headings()[0].title.strip() == 'Streams':
				tbl = section.split('\n')
				lines = []
				for line in tbl:
					match = re.search(re_find, line)
					if not match:
						lines.append(line)
						continue
					if match[3] in STREAM_NAMES:
						lines.append(re.sub(re_find, re_repl_no_display, line))
					else:
						lines.append(re.sub(re_find, re_repl_display, line))
				wikitext.replace(section, '\n'.join(lines))
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)