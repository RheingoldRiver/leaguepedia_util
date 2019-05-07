from log_into_wiki import *
import mwparserfromhell, re
limit = -1

game_args = ['requires','ranks','effects','baseid']
global_args = ['image','image desc']
game_lookup = {
	'fo1' : 'Fallout',
	'fo2' : 'Fallout 2',
	'fo3' : 'Fallout 3',
	'fo3bs' : 'Broken Steel',
	'fo3mz' : 'Mothership Zeta (add-on)',
	'fo3oa' : 'Operation: Anchorage (add-on)',
	'fo3pl' : 'Point Lookout (add-on)',
	'fo3tp' : 'The Pitt (add-on)',
	'fo4' : 'Fallout 4',
	'fo4am' : 'Automatron',
	'fo4ww' : 'Wasteland Workshop',
	'fo4fh' : 'Far Harbor',
	'fo4cw' : 'Contraptions Workshop',
	'fo4vw' : 'Vault-Tec Workshop',
	'fo4nw' : 'Nuka-World',
	'f76' : 'Fallout 76',
	'fs' : 'Fallout Shelter',
	'foww' : 'Fallout: Wasteland Warfare',
	'fobos' : 'Fallout: Brotherhood of Steel',
	'fobos2' : 'Fallout:Brotherhood of Steel 2',
	'fool' : 'Fallout Online',
	'fot' : 'Fallout Tactics',
	'fot2': 'Fallout Tactics 2',
	'fow' : 'Fallout: Warfare',
	'lh' : 'Lionheart',
	'fnv' : 'Fallout: New Vegas',
	'jes' : "J.E. Sawyer's Fallout RPG",
	'vb' : 'Van Buren',
	'v13' : 'Project V13',
	'torn' : 'TORN',
	'tar' : 'The Armageddon Rag',
	'pa' : 'One Man, and a Crate of Puppets',
	'fos' : 'Fallout Shelter',
	'fox' : 'Fallout Extreme',
	'fnvdm' : 'Dead Money',
	'fnvhh' : 'Honest Hearts',
	'fnvowb' : 'Old World Blues',
	'fnvlr' : 'Lonesome Road',
	'fnvgra' : "Gun Runners' Arsenal"
	
	
	# todo: maybe add more of these if needed
	
}

games_to_skip = [ 'Fallout: Brotherhood of Steel', 'Fallout:Brotherhood of Steel 2' ]

site = login("me","fallout")

infobox = site.pages['Template:Infobox perk']
pages = infobox.embeddedin()
conflicts = []

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

startat_player = 'Scourge of the East'

try:
	startat = pages_array.index(startat_player)
except NameError as e:
	startat = -1
print('Starting at: ' + str(startat))

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat or page.name.startswith('User:') :
		print("Skipping page %s" % page.name)
	else:
		print('Processing page %s...' % page.name)
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		games = []
		games_dict = {}
		navbox_dict = {}
		for template in wikitext.filter_templates():
			if template.name.matches('Infobox perk'):
				for i in range(1,11):
					if template.has('games' + str(i)):
						tl = mwparserfromhell.nodes.template.Template('Infobox perk game')
						for arg in game_args:
							if template.has(arg + str(i)):
								tl.add(arg, template.get(arg + str(i)).value)
						for arg in global_args:
							if template.has(arg):
								tl.add(arg, template.get(arg).value)
						this_games = re.split('\s*,\s*', template.get('games' + str(i)).value.strip() )
						for this_game in this_games:
							this_game_actual = game_lookup[this_game.lower()]
							if this_game_actual not in games:
								games.append(this_game_actual)
								games_dict[this_game_actual] = str(tl)
								navbox_dict[this_game_actual] = '{{Navbox perks %s}}' % this_game
							else:
								conflicts.append(page.name)
				wikitext.remove(template)
				break
		rest_of_text = str(wikitext)
		rest_of_text = rest_of_text.split('{{Navbox perks')[0]
		for game in games:
			if game not in games_to_skip:
				p = site.pages[page.name + '/' + game]
				print('Saving page %s...' % p.name)
				p.save('{{PerksTabsHeader}}\n' + games_dict[game] + rest_of_text + navbox_dict[game], summary = 'Attempting to auto-split perk page')
		


print('Printing conflicts (pages with the same game listed more than once)...')
for conflict in conflicts:
	print(conflict)