import re
import mwparserfromhell

lookup_table = { 
	{ "keystone": "Resolve", "secondary": "Kleptomancy" },
	{ "keystone": "Inspiration", "secondary": "Aftershock" },
	{ "keystone": "Precision", "secondary": "Arcane Comet" },
	{ "keystone": "Sorcery", "secondary": "Kleptomancy" },
	{ "keystone": "Resolve", "secondary": "Unsealed Spellbook" },
	{ "keystone": "Resolve", "secondary": "Unsealed Spellbook" },
	{ "keystone": "Inspiration", "secondary": "Electrocute" },
	{ "keystone": "Sorcery", "secondary": "Unsealed Spellbook" },
	{ "keystone": "Precision", "secondary": "Unsealed Spellbook" },
	{ "keystone": "Resolve", "secondary": "Unsealed Spellbook" },
}

content = ""
with open("data.txt") as f:
 content = f.read()

wikicode = mwparserfromhell.parse(content)
templates = wikicode.filter_templates(recursive=False)
for t in templates:
	if t.name == MatchRecapS8:
		mh = t.get("statslink")
		gameID = re.search("(\d*)\?gameHash",mh)
		k = 1
		for i in ["blue","red"]
			for j in range (1,5):
				keystone = lookup_table[gameID][k]["keystone"]
				secondary = lookup_table[gameID][k]["keystone"]
				player = t.get(i+j).filter_templates()
				player.remove("keystone")
				player.remove("secondary")
				player.add("keystone",keystone)
				player.add("secondary",secondary)
				k = k + 1
output = str(templates)
print(output)

things_you_want_to_add_to = [t for t in templates    if len(t.split("keystone")) == 2]
thing_you_want_to_add_to = things_you_want_to_add_to[0]
thing_you_want_to_add_to.get('keystone').value = "the value you want to change to"






import re
import mwparserfromhell

content = ""
with open("data.txt") as f:
 content = f.read()

wikicode = mwparserfromhell.parse(content)
templates = wikicode.filter_templates()
things_you_want_to_add_to = [t for t in templates    if len(t.split("keystone")) == 2]
thing_you_want_to_add_to = things_you_want_to_add_to[0]
thing_you_want_to_add_to.get('keystone').value = "the value you want to change to"

lookup_table = {
  "1234": {
    "papryze": {
      "keystone": "kelptomancy",
      "secondary": "idontfuckingknow",
    },
    "swathe": {
      "keystone": "aftershock",
      "secondary": "whothefuckcares"
    }
  }
}

def parse_game_id_from_statslink(statslink):
  #river fill this in
  pass

for template in templates:
  if len(t.split("keystone")) > 2:
    # we are in the game template which contains all the player info, which is why we found keystone more than once
    game_id = parse_game_id_from_statslink(template.get('statslink'))
  if len(t.split("keystone")) == 2:
    # we are in a "base template" - we want to edit this
    player_name = template.get('name').strip()
    template.get('keystone').value = lookup_table[game_id][player_name]['keystone']
    template.get('secondary').value = lookup_table[game_id][player_name]['secondary']

# literally copy and paste this output into MW and you're done
print template