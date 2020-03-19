from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'blank predictions of rescheduled games'  # Set summary

PARAMS = [
"t6_r1",
"t6_r1_order",
"t6_r2",
"t6_r2_order",
"t6_r3",
"t6_r3_order",
"t6_r4",
"t6_r4_order",
"t6_r5",
"t6_r5_order",
"t6_r6",
"t6_r6_order",
"t6_r7",
"t6_r7_order",
"t6_r8",
"t6_r8_order",
"t7_r1",
"t7_r1_order",
"t7_r2",
"t7_r2_order",
"t7_r3",
"t7_r3_order",
"t7_r4",
"t7_r4_order",
"t7_r5",
"t7_r5_order",
"t7_r6",
"t7_r6_order",
"t7_r7",
"t7_r7_order",
"t7_r8",
"t7_r8_order",
"t8_r1",
"t8_r1_order",
"t8_r2",
"t8_r2_order",
"t8_r3",
"t8_r3_order",
"t8_r4",
"t8_r4_order",
"t8_r5",
"t8_r5_order",
"t8_r6",
"t8_r6_order",
"t8_r7",
"t8_r7_order",
"t8_r8",
"t8_r8_order",
"t9_r1",
"t9_r1_order",
"t9_r2",
"t9_r2_order",
"t9_r3",
"t9_r3_order",
"t9_r4",
"t9_r4_order",
"t9_r5",
"t9_r5_order",
"t9_r6",
"t9_r6_order",
"t9_r7",
"t9_r7_order",
"t9_r8",
"t9_r8_order",
"t10_r1",
"t10_r1_order",
"t10_r2",
"t10_r2_order",
"t10_r3",
"t10_r3_order",
"t10_r4",
"t10_r4_order",
"t10_r5",
"t10_r5_order",
"t10_r6",
"t10_r6_order",
"t10_r7",
"t10_r7_order",
"t10_r8",
"t10_r8_order",
]

for page in site.cargo_client.page_list(
	tables="UserPredictions",
	fields="_pageName=Page",
	where='OverviewPage="LCK/2020 Season/Spring Season"'):
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		for param in PARAMS:
			if template.has(param):
				template.remove(param)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
