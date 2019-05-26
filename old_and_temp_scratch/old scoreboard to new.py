from log_into_wiki import *
from template_list import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Updating scoreboards!?!?!?!!?!?!!? MatchRecapS4/Header'  # Set summary

limit = -1

this_year_number = '4'
no_smw = False

no_smw_suffix = 'NoSMW' if no_smw else ''
this_template_name = 'Template:MatchRecapS4/Header' + this_year_number + no_smw_suffix

this_template_name = 'Template:MatchRecapS4/Header'
# startat_page = 'asdf'
this_template = site.pages[this_template_name]  # Set template
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

def fixGold(template, param):
	param = param if param else 'gold'
	if template.has(param):
		gold = template.get(param).value.strip()
		if gold != '':
			goldInt = float(gold)
			if (param == 'gold' and goldInt < 500) or goldInt < 1000:
				actualGold = int(goldInt * 1000)
				template.add(param, str(actualGold))
def getTZ(template, tz):
	if template.has(tz):
		val = template.get(tz).value.strip()
		if val != '':
			return val
	return False
def fixTimezones(template):
	time = ''
	tz = ''
	for tz in ['PST', 'KST', 'CET']:
		time = getTZ(template, tz)
		if time:
			break
	template.add('timezone', tz, before = tz)
	template.add('time', time, before = tz)
	template.remove(tz)
def fixPurple(template):
	i = 1
	s = str(i)
	while template.has('purple' + s):
		template.get('purple' + s).name = 'red' + s
		i += 1
		s = str(i)
def fixVOD(template):
	if template.has('lolvod'):
		vod = template.get('lolvod').value.strip()
		template.add('vodlink', vod, before='lolvod')
		template.remove('lolvod')
this_year = 'MatchRecapS' + this_year_number

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		print(page.name)
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			name = template.name.strip()
			if 'Ultimate' in name:
				pass
			elif template.name.matches(this_year) or template.name.matches(this_year + 'NoSMW') or name == 'MatchRecapS4/2v2' or name == 'MatchRecapS4/1v1':
				fixPurple(template)
				if template.name.matches(this_year + 'NoSMW'):
					template.add('nocargo','Yes')
				template.name = 'Scoreboard/Season ' + this_year_number
				fixGold(template, 'team1g')
				fixGold(template, 'team2g')
				fixTimezones(template)
				fixVOD(template)
				if name == 'MatchRecapS4/2v2':
					template.add('teamsize',2)
					template.add('nocargo', 'Yes')
				if name == 'MatchRecapS4/1v1':
					template.add('teamsize',1)
					template.add('nocargo', 'Yes')
			elif 'MatchRecap' in name and '/Player' in name:
				if 'NoSMW' in name:
					template.add('nocargo','Yes')
				template.name = 'Scoreboard/Player'
				fixGold(template, 'gold')
			elif template.name in scoreboard_button_templates:
				template.name = 'Scoreboard/Button'
			elif 'MatchRecap' in name and '/Header' in name:
				template.name = 'Scoreboard/Header'
			elif template.name.matches('TOCRight'):
				template.name = 'TOCFlat'
			elif template.name.matches('MatchRecapNoItems'):
				template.add('noitems','yes')
				if template.has('purple1'):
					template.get('purple1').name = 'red1'
					template.get('purple2').name = 'red2'
					template.get('purple3').name = 'red3'
					template.get('purple4').name = 'red4'
					template.get('purple5').name = 'red5'
				if template.name.matches(this_year + 'NoSMW'):
					template.add('nocargo','Yes')
				template.name = 'Scoreboard/Season ' + this_year_number
				if template.has('lolvod'):
					vod = template.get('lolvod').value.strip()
					template.add('vodlink', vod, before = 'lolvod')
					template.remove('lolvod')
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)