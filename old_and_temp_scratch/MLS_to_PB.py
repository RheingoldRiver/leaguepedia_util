import mwparserfromhell, mwclient, re
from log_into_wiki import *

limit = -1

regorder = { "bluebans":[2, 4, 6],
			 "redbans":[3, 5, 7],
			 "bluepicks":[8, 11, 12, 15, 16],
			 "redpicks":[9, 10, 13, 14, 17],
			 "nbans":3
			 }

# for some reason old pick-bans are sometimes shown with red side on the left ?_?
vsorder = { "redbans":[2, 4, 6],
			 "bluebans":[3, 5, 7],
			 "redpicks":[8, 11, 12, 15, 16],
			 "bluepicks":[9, 10, 13, 14, 17],
			 "nbans":3
			 }

# waaay old games - not supported yet because the current module doesn't include support for this even....
oldregorder = { "bluebans":[2, 5],
			 "redbans":[3, 4],
			 "bluepicks":[6, 9, 10, 13, 14],
			 "redpicks":[7, 8, 11, 12, 15],
			 "nbans":2
			 }

argorder = [ "noroles", "nocargo", "team1", "team2", "team1score", "team2score", "winner", "blueban1", "red_ban1", "blueban2", "red_ban2", "blueban3", "red_ban3", "bluepick1", "red_pick1", "red_pick2", "bluepick2", "bluepick3", "red_pick3", "red_pick4", "bluepick4", "bluepick5", "red_pick5"]
deletethese = ["MatchListSlot","MatchListEnd"]

thispage = site.pages["Template:MatchListStart"]
pages = thispage.embeddedin(namespace=0)

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt = lmt + 1
	text = page.text()
	text = text.replace("{{MatchListEnd}}","{{MatchListEnd}}\n").replace("{{MatchListEnd}}\n{{MatchListEnd}}\n","{{MatchListEnd}}\n")
	print(page.name)
	wikitext = mwparserfromhell.parse(text)
	templates = wikitext.filter_templates(recursive=False)
	broken = False
	for i in range(len(templates)):
		if templates[i].name.strip() == "MatchListStart":
			broken = False
			try:
				parsed = {
					'noroles':'yes',
					'nocargo':'yes'
				}
				d = regorder
				if templates[i + 2].get(1).strip() != "":
					parsed['team1'] = templates[i+1].get(1).value.strip("' ")
					parsed['team2'] = templates[i+1].get(2).value.strip("' ")
					parsed['team1score'] = templates[i+1].get("games1").value.strip()
					parsed['team2score'] = templates[i+1].get("games2").value.strip()
					parsed['winner'] = templates[i+1].get("win").value.strip()
				else:
					parsed['team2'] = templates[i + 1].get(1).value.strip("' ")
					parsed['team1'] = templates[i + 1].get(2).value.strip("' ")
					parsed['team2score'] = templates[i + 1].get("games1").value.strip()
					parsed['team1score'] = templates[i + 1].get("games2").value.strip()
					parsed['winner'] = 3 - int(templates[i + 1].get("win").value.strip())
					d = vsorder
				for k in range(d["nbans"]):
					v1 = templates[i + d["bluebans"][k]].get(1).value
					v2 = templates[i + d["redbans"][k]].get(2).value
					v1str = str(v1).strip("' ").lower()
					v2str = str(v2).strip("' ").lower()
					if v1str == "none" or v1str == 'no ban':
						parsed['blueban' + str(k + 1)] = "None"
					elif v1str == "":
						parsed['blueban' + str(k + 1)] = "Unknown"
					elif v1str == "loss of ban":
						parsed['blueban' + str(k + 1)] = "Loss of Ban"
					else:
						parsed['blueban' + str(k + 1)] = v1.filter_templates()[0].get(1).value.strip()
					if v2str == "none" or v1str == 'no ban':
						parsed['redban' + str(k + 1)] = "None"
					elif v2str == "":
						parsed['red_ban' + str(k + 1)] = "Unknown"
					elif v2str == "loss of ban":
						parsed['red_ban' + str(k + 1)] = "Loss of Ban"
					else:
						parsed['red_ban' + str(k+1)] = v2.filter_templates()[0].get(1).value.strip()
				for k in range(5):
					v1 = templates[i + d["bluepicks"][k]].get(1).value.filter_templates()[0].get(1).value.strip()
					v2 = templates[i + d["redpicks"][k]].get(2).value.filter_templates()[0].get(1).value.strip()
					parsed['bluepick' + str(k+1)] = v1
					parsed['red_pick' + str(k+1)] = v2
				templates[i].remove(1)
				templates[i].remove('width')
				for arg in argorder:
					templates[i].add(arg,parsed[arg])
				templates[i].name = "PicksAndBans"
			except Exception as e:
				broken = True
		elif templates[i].name.strip() in deletethese and not broken:
			for param in templates[i].params:
				templates[i].remove(param.name)
			templates[i].name = "delete"
	if len(wikitext.filter_headings()) >= 1:
		wikitext.insert_before(wikitext.filter_headings()[0],"{{PicksAndBans/Button}}\n")
	newtext = re.sub('\\{\\{delete.*\\}\\}\s*','',str(wikitext))
	newtext = newtext.replace("{{PicksAndBans/Button}}\n{{PicksAndBans/Button}}\n","{{PicksAndBans/Button}}\n")
	if newtext != text:
		print("Saving...")
		page.save(newtext,summary="Updating to new Picks & Bans template automatically",tags="new_pickban")
	else:
		print("No changes, skipping")