from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

champions = [
	"neeko",
	"nunu & willump",
	"rift scuttler",
	"pyke",
	"kai'sa",
	"kayn",
	"zoe",
	"ornn",
	"rakan",
	"xayah",
	"camille",
	"ivern",
	"kled",
	"taliyah",
	"aurelion sol",
	"illaoi",
	"jhin",
	"aatrox",
	"ahri",
	"akali",
	"alistar",
	"amumu",
	"anivia",
	"annie",
	"ashe",
	"azir",
	"bard",
	"blitzcrank",
	"brand",
	"braum",
	"caitlyn",
	"cassiopeia",
	"cho'gath",
	"corki",
	"darius",
	"diana",
	"dr. mundo",
	"draven",
	"ekko",
	"elise",
	"evelynn",
	"ezreal",
	"fiddlesticks",
	"fiora",
	"fizz",
	"galio",
	"gangplank",
	"garen",
	"gnar",
	"gragas",
	"graves",
	"hecarim",
	"heimerdinger",
	"irelia",
	"janna",
	"jarvan iv",
	"jax",
	"jayce",
	"jinx",
	"kalista",
	"karma",
	"karthus",
	"kassadin",
	"katarina",
	"kayle",
	"kennen",
	"kha'zix",
	"kindred",
	"kog'maw",
	"leblanc",
	"lee sin",
	"leona",
	"lissandra",
	"lucian",
	"lulu",
	"lux",
	"malphite",
	"malzahar",
	"maokai",
	"master yi",
	"miss fortune",
	"mordekaiser",
	"morgana",
	"nami",
	"nasus",
	"nautilus",
	"nidalee",
	"nocturne",
	"nunu",
	"olaf",
	"orianna",
	"pantheon",
	"poppy",
	"quinn",
	"rammus",
	"rek'sai",
	"renekton",
	"rengar",
	"riven",
	"rumble",
	"ryze",
	"sejuani",
	"shaco",
	"shen",
	"shyvana",
	"singed",
	"sion",
	"sivir",
	"skarner",
	"sona",
	"soraka",
	"swain",
	"syndra",
	"tahm kench",
	"talon",
	"taric",
	"teemo",
	"thresh",
	"tristana",
	"trundle",
	"tryndamere",
	"twisted fate",
	"twitch",
	"udyr",
	"urgot",
	"varus",
	"vayne",
	"veigar",
	"vel'koz",
	"vi",
	"viktor",
	"vladimir",
	"volibear",
	"warwick",
	"wukong",
	"xerath",
	"xin zhao",
	"yasuo",
	"yorick",
	"zac",
	"zed",
	"ziggs",
	"zilean",
	"zyra",
	"dragon",
	"rift herald",
	"baron nashor"
]

runes = [
	"overgrowth",
	"ravenous hunter",
	"shield bash",
	"time warp tonic",
	"sudden impact",
	"domination",
	"celerity",
	"minion dematerializer",
	"the ultimate hat",
	"hail of blades",
	"ultimate hunter",
	"nimbus cloak",
	"cheap shot",
	"ingenious hunter",
	"demolish",
	"presence of mind",
	"legend tenacity",
	"cut down",
	"absolute focus",
	"precision",
	"inspiration",
	"resolve",
	"conqueror",
	"bone plating",
	"chrysalis",
	"iron skin",
	"mirror shell",
	"kleptomancy",
	"coup de grace",
	"last stand",
	"triumph",
	"ghost poro",
	"manaflow band",
	"scorch",
	"predator",
	"zombie ward",
	"press the attack",
	"lethal tempo",
	"fleet footwork",
	"electrocute",
	"predator",
	"dark harvest",
	"summon aery",
	"arcane comet",
	"phase rush",
	"aftershock",
	"guardian",
	"unsealed spellbook",
	"glacial augment",
	"kleptomancy"
]

masteries = [
	"adaptive armor",
	"alchemist",
	"arcane blade",
	"arcane mastery",
	"archmage",
	"bandit",
	"blade weaving",
	"bladed armor",
	"block",
	"brute force",
	"butcher",
	"culinary master",
	"dangerous game",
	"devastating strikes",
	"double edged sword",
	"enchanted armor",
	"evasive",
	"executioner",
	"expanded mind",
	"expose weakness",
	"feast",
	"fleet of foot",
	"frenzy",
	"fury",
	"greed",
	"hardiness",
	"havoc",
	"inspiration",
	"intelligence",
	"juggernaut",
	"legendary guardian",
	"martial mastery",
	"meditation",
	"mental force",
	"oppression",
	"perseverance",
	"phasewalker",
	"recovery",
	"reinforced armor",
	"resistance",
	"runic affinity",
	"runic blessing",
	"scavenger",
	"scout",
	"second wind",
	"sorcery",
	"spell weaving",
	"strength of spirit",
	"summoner's insight",
	"swiftness",
	"tenacious",
	"tough skin",
	"unyielding",
	"vampirism",
	"veteran's scars",
	"wanderer",
	"warlord",
	"wealth",
	"assassin",
	"bandit",
	"battering blows",
	"bond of stone",
	"bounty hunter",
	"dangerous game",
	"deathfire touch",
	"double edged sword",
	"explorer",
	"expose weakness",
	"feast",
	"fervor of battle",
	"fury",
	"grasp of the undying",
	"insight",
	"intelligence",
	"legendary guardian",
	"meditation",
	"merciless",
	"natural talent",
	"oppressor",
	"perseverance",
	"piercing thoughts",
	"precision",
	"recovery",
	"runic affinity",
	"runic armor",
	"savagery",
	"secret stash",
	"sorcery",
	"stormraider's surge",
	"strength of the ages",
	"swiftness",
	"thunderlord's decree",
	"tough skin",
	"unyielding",
	"vampirism",
	"veteran's scars",
	"wanderer",
	"warlord's bloodlust",
	"windspeaker's blessing",
	"assassin",
	"bandit",
	"battering blows",
	"battle trance",
	"bond of stone",
	"bounty hunter",
	"courage of the colossus",
	"dangerous game",
	"deathfire touch",
	"double edged sword",
	"explorer",
	"expose weakness",
	"fearless",
	"feast",
	"fervor of battle",
	"fresh blood",
	"fury",
	"grasp of the undying",
	"greenfather's gift",
	"insight",
	"intelligence",
	"legendary guardian",
	"meditation",
	"merciless",
	"natural talent",
	"perseverance",
	"piercing thoughts",
	"precision",
	"recovery",
	"runic affinity",
	"runic armor",
	"savagery",
	"secret stash",
	"siegemaster",
	"sorcery",
	"stoneborn pact",
	"stormraider's surge",
	"swiftness",
	"thunderlord's decree",
	"tough skin",
	"unyielding",
	"vampirism",
	"veteran's scars",
	"wanderer",
	"warlord's bloodlust",
	"windspeaker's blessing"
]

stats = ['lifesteal items', 'critical strike items']

summoners = ['barrier', 'clairvoyance', 'clarity', 'cleanse', 'exhaust', 'flash', 'garrison', 'ghost', 'heal', 'ignite', 'mark dash', 'mark', 'smite', 'teleport', 'promote', 'revive', 'surge']

fuckgrasp = ['grasp of the undying2']

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:PTOC']  # Set template
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
			if template.name.matches('PTOC'):
				if template.has('1'):
					val = template.get('1').value.strip()
					lc = val.lower()
					if lc in champions:
						template.name = 'PTOC/Champ'
					elif lc in runes:
						template.name = 'PTOC/Rune'
					elif lc in masteries:
						template.name = 'PTOC/Mastery'
					elif lc in fuckgrasp:
						template.add('1', 'Grasp of the Undying')
						template.name = 'PTOC/Rune'
					elif lc in stats:
						template.name = 'PTOC/Stat'
						template.add('1', val.sub(' items',''))
					elif lc in summoners:
						template.name = 'PTOC/Summoner'
					else:
						template.name = 'PTOC/Item'
					val_new = template.get('1').value.strip()
					val_new = val_new.replace('  ',' ')
					val_new = val_new.replace('Enchantment: ', 'Enchantment - ')
					template.add('1', val_new)
			
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)