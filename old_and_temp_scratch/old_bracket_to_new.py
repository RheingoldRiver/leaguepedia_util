from log_into_wiki import *
import mwparserfromhell, math

site = login('me', 'cod-esports')  # Set wiki

################################################################
this_bracket = '4SE'
matches_to_add = {
	'R2D1' : 'third'
}
replacement_team_numbers = {
	'R2D1' : 3,
	'R2D2' : 4
}
old_bracket = False#'8SEBracketMatchInfo'

summary = 'Change to new brackets (%s)' % this_bracket  # Set summary
limit = 2
# startat_page = 'asdf'
this_template = site.pages['Template:%sBracket' % this_bracket]  # Set template
bracket_to_match = '%sBracket' % this_bracket
if old_bracket:
	print(this_template) # fuck you pycharm "error" highlighting
	print(bracket_to_match)
	this_template = site.pages['Template:' + old_bracket]
	bracket_to_match = old_bracket
pages = this_template.embeddedin()

pages_var = list(pages)

#pages_var = [site.pages['International Wildcard All-Star Melbourne 2015']]

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
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
		text = text.replace('Template:' + this_bracket + 'Bracket', this_bracket + 'Bracket')
		wikitext = mwparserfromhell.parse(text, skip_style_tags=True)
		sup_error = False
		for template in wikitext.filter_templates():
			conflicting_field_error = False
			if template.name.matches(bracket_to_match):
				used = {}
				template.name = 'Bracket'
				template.add(1,this_bracket)
				if template.has('name-width'):
					template.remove('name-width')
				if template.has('hideroundtitles') and template.get('hideroundtitles').value.strip() == 'true':
					template.add('notitle','yes')
				for r_int in range(1,12):
					r = str(r_int)
					if template.has('R' + r):
						title = template.get('R' + r).value.strip()
						template.add('R' + r + '_title', title)
						template.remove('R' + r)
					for t_int in range(1,64):
						t = str(t_int)
						for l in ['W','D','L']:
							match_id = 'R' + r + l + t
							if template.has(match_id) or template.has(match_id + 'team') or template.has(match_id + 'literal'):
								val = ''
								bye = False
								is_from_team = False
								if template.has(match_id):
									val = template.get(match_id).value.strip()
									template.remove(match_id, False)
								elif template.has(match_id + 'team'):
									val = template.get(match_id + 'team').value.strip()
									template.remove(match_id + 'team', False)
									is_from_team = True
								elif template.has(match_id + 'literal'):
									val = template.get(match_id + 'literal').value.strip()
								if match_id in matches_to_add and val != '' and not re.match(r'{{[tT]eam(Short)?\|?\s*(\|rightshort(linked)?)?\}\}', val):
									template.add(matches_to_add[match_id], 'Yes')
								winner = False
								if "'''" in val:
									winner = True
								if template.has(match_id + 'win'):
									if template.get(match_id + 'win').value.strip() != '':
										winner = True
									template.remove(match_id + 'win')
								val = val.replace("'''",'')
								n = 0
								this_team = ''
								footenoten = False
								player = False
								playerlink = False
								flag = False
								playerflag = False
								champion = False
								score = False
								if is_from_team:
									this_team = val
									n = 1
								else:
									if val == 'BYE':
										bye = True
									elif val == '':
										pass
									else:
										val_wikitext = mwparserfromhell.parse(val)
										n = 0
										for tl in val_wikitext.filter_templates():
											if tl.name.matches('flag') or tl.name.matches('TeamPositionChampionSwap'):
												break
											if tl.name.matches('player'):
												player = tl.get(1).value.strip()
												if tl.has('link'):
													playerlink = tl.get('link').value.strip()
												if tl.has('flag'):
													playerflag = tl.get('flag').value.strip()
											elif tl.name.matches('ci'):
												champion = tl.get(1).value.strip()
												val = re.sub(r'{{ci\|.+?\}\}','',val)
											else:
												n += 1
												if tl.has(1):
													this_team = tl.get(1).value.strip()
										for tag in val_wikitext.filter_tags():
											if str(tag.tag) == 'sup':
												footenoten = str(tag.contents)
										if n > 0:
											for link in val_wikitext.filter_wikilinks():
												player = link.text or link.title
												if link.text:
													playerlink = link.title
								if template.has(match_id + 'score'):
									score = template.get(match_id + 'score').value.strip()
									if "'''" in score:
										winner = True
									score = score.replace("'''","")
									if 'sup' in score:
										sup_error = True
									template.remove(match_id + 'score', False)
									if score == '':
										score = False
								if template.has(match_id + 'flag'):
									flag = template.get(match_id + 'flag').value.strip()
									if flag == '':
										flag = False
									template.remove(match_id + 'flag')
								team = 1
								t_int_actual = t_int
								if match_id in replacement_team_numbers:
									t_int_actual = replacement_team_numbers[match_id]
								if t_int_actual % 2 == 0:
									team = 2
								match = math.floor((t_int_actual + 1) / 2)
								new_match_id = 'R' + r + 'M' + str(match)
								if new_match_id in used:
									conflicting_field_error = True
								ts = str(team)
								used[new_match_id + ts] = True
								#print(match_id + ' - ' + new_match_id + ts)
								if bye:
									template.add(new_match_id + '_bye_' + ts,'yes')
								else:
									if n > 0:
										template.add(new_match_id + '_team_' + ts, this_team)
									else:
										template.add(new_match_id + '_literal_' + ts, val)
										if 'sup' in val:
											sup_error = True
									if score:
										template.add(new_match_id + '_score_' + ts, score)
									if flag:
										template.add(new_match_id + '_flag_' + ts, flag)
									if playerflag:
										template.add(new_match_id + '_playerflag_' + ts, playerflag)
									if winner:
										template.add(new_match_id + '_winner', team)
									if footenoten:
										template.add(new_match_id + '_footnoten_' + ts, footenoten)
									if player:
										template.add(new_match_id + '_player_' + ts, player)
										template.add('teamstyle', 'onlyimagelinkedshort')
									if playerlink:
										template.add(new_match_id + '_playerlink_' + ts, playerlink)
									if champion:
										template.add(new_match_id + '_champion_' + ts, champion)
		newtext = str(wikitext).replace('&#124;','|')
		if sup_error:
			newtext = newtext + '\n[[Category:Brackets With Sup Errors]]'
		# if conflicting_field_error:
		# 	newtext = newtext + '\n[[Category:Brackets With Conflicting Field Errors]]'
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary, tags = 'new_brackets')
		else:
			print('Skipping page %s...' % page.name)