from esportswiki_editing import *
import mwparserfromhell, re

site = login('me', 'lol')  # Set wiki
summary = 'Discover & auto-add vods to SB'  # Set summary

vod_params = ['vodpb', 'vodstart', 'vod']

def add_vod(template, tl, arg):
	template.add('vodlink', tl.get(arg).value.strip())

def data_suffix(n):
	if n == 1:
		return ''
	return '/' + str(n)

def process_pages(data_page_name, sb_page_name):
	data_page = site.pages[data_page_name]
	data_text = data_page.text()
	data_wikitext = mwparserfromhell.parse(data_text)
	sb_page = site.pages[sb_page_name]
	sb_text = sb_page.text()
	sb_wikitext = mwparserfromhell.parse(sb_text)
	for template in sb_wikitext.filter_templates():
		if template.has('statslink'):
			mh = template.get('statslink').value.strip()
			re_match = re.search(r'match-details/([A-Za-z0-9]+/[0-9]+)', mh)
			if not re_match:
				continue
			match_id = re_match[1]
			print(match_id)
			for tl in data_wikitext.filter_templates():
				if tl.has('mh'):
					if match_id in tl.get('mh').value.strip():
						for vod in vod_params:
							if tl.has(vod) and tl.get(vod).value.strip() != '':
								print('has: %s' % vod)
								add_vod(template, tl, vod)
								break
						break
	if str(sb_wikitext) != sb_text:
		sb_page.save(str(sb_wikitext), summary = summary)

result = site.cargoquery(
	tables="MatchScheduleGame=MSG,ScoreboardGame=SG",
	join_on="MSG.ScoreboardID_Wiki=SG.ScoreboardID_Wiki",
	where="SG.VOD IS NULL AND SG._pageName IS NOT NULL AND (MSG.Vod IS NOT NULL OR MSG.VodPostgame IS NOT NULL OR MSG.VodPB IS NOT NULL) AND MSG.MatchHistory IS NOT NULL",
	fields="SG._pageName=SBPage,MSG._pageName=MSGPage",
	group_by="SG._pageName",
	limit=5000
)

for item in result:
	process_pages(item['MSGPage'], item['SBPage'])
