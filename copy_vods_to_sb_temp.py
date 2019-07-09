from log_into_wiki import *
import mwparserfromhell

##############################################
##############################################
tournament = 'LCS 2019 Spring' # this should redirect to the tournament
data_page_number = 2
sb_page_name = 'LCS/2019 Season/Spring Season/Scoreboards/Week 9'
##############################################
##############################################

site = login('me', 'lol')  # Set wiki
summary = 'Auto-add vods to SB'  # Set summary

vod_params = ['vodpb', 'vodstart']

def add_vod(template, tl, arg):
	template.add('vodlink', tl.get(arg).value.strip())

def data_suffix(n):
	if n == 1:
		return ''
	return '/' + str(n)

overview_page = site.pages[tournament].redirects_to()
data_page = site.pages['Data:' + overview_page.name + data_suffix(data_page_number)]
data_text = data_page.text()
data_wikitext = mwparserfromhell.parse(data_text)
sb_page = site.pages[sb_page_name]
sb_text = sb_page.text()
sb_wikitext = mwparserfromhell.parse(sb_text)
for template in sb_wikitext.filter_templates():
	if template.has('statslink'):
		mh = template.get('statslink').value.strip()
		match_id = re.search(r'match-details/([A-Za-z0-9]+/[0-9]+)', mh)[1]
		print(match_id)
		for tl in data_wikitext.filter_templates():
			if tl.has('mh'):
				if match_id in tl.get('mh').value.strip():
					for vod in vod_params:
						if tl.has(vod):
							add_vod(template, tl, vod)
							break
if str(sb_wikitext) != sb_text:
	print('Changes made, saving...')
	sb_page.save(str(sb_wikitext), summary = summary)
