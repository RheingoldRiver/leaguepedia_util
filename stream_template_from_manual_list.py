from log_into_wiki import *
import mwparserfromhell, time

site = login('bot','lol') # Set wiki
summary = 'Converting streams to use stream template (incl in infobox)' # Set summary

limit = -1
#startat_page = 'Liga de Videojuegos Profesional/Season 8/Sprint 2'
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

SECTION_NAMES = ['Streams', 'View Games', 'Video Channels']

re_find = r'\{\{flag\|\s*(\w+)\s*\}\}\s*\[([^\s]*) (.+?)\]'
re_repl_no_display = r'{{stream|url=\2|lang=\1}}'
re_repl_display = r'{{stream|url=\2|lang=\1|display=\3}}'

def replace_stream_text(text):
	match = re.search(re_find, text)
	if not match:
		return text
	if match[3] in STREAM_NAMES:
		return re.sub(re_find, re_repl_no_display, text)
	else:
		return re.sub(re_find, re_repl_display, text)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
		continue
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for section in wikitext.get_sections():
		if section.filter_headings() and section.filter_headings()[0].title.strip() in SECTION_NAMES:
			tbl = section.split('\n')
			lines = []
			for line in tbl:
				lines.append(replace_stream_text(line))
			wikitext.replace(section, '\n'.join(lines))
	for template in wikitext.filter_templates():
		if template.name.matches('Infobox Tournament'):
			if template.has('streams'):
				val = template.get('streams').value.strip()
				val_new = replace_stream_text(val)
				template.add('streams', val_new)
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		# time.sleep(0.1)
		print('Skipping page %s...' % page.name)