import re
with open('vg teamnames.txt', encoding="utf-8") as f:
	lines = f.readlines()
lines = [line.strip() for line in lines]

teamdata = {}
teamnames = []

for line in lines:
	line_tbl = re.split('=',line)
	line_tbl = [part.strip('" |') for part in line_tbl]
	if len(line_tbl) == 2:
		thisteam = line_tbl[1] if re.match('^[^{}]*$',line_tbl[1]) else line_tbl[0]
		if thisteam in teamdata.keys():
			teamdata[thisteam]['names'].append(line_tbl[0])
		else:
			teamdata[thisteam] = {
				'names': [thisteam]
			}
			teamnames.append(thisteam)
		if re.match('.*vardefine.*',line_tbl[1]):
			data = line_tbl[1].strip()
			teamvars = re.split('\{\{\#vardefine:([^\}]*)\}\}',data)
			for var in teamvars:
				if re.match('.*\|.*',var):
					var_info = re.split('\|',var)
					teamdata[thisteam][var_info[0]] = var_info[1]

# group teams together by looking up link. keep it keyed by team though because I'm lazy and didn't want to rewrite
# the section after this when I realized I needed this
# sorry future me
linkdata = {}
linknames = []
linksused = {} # yeah 2 dictionaries here bc of laziness
for team in teamnames:
	link = teamdata[team]['teamLink']
	if link in linksused.keys():
		thisteam = linksused[link]
		linkdata[thisteam]['names'].append(team)
	else:
		linkdata[team] = {
			'names' : teamdata[team]['names'],
			'teamLink' : teamdata[team]['teamLink'],
			'teamLong': teamdata[team]['teamLong'],
			'teamShort': teamdata[team]['teamShort']
		}
		linknames.append(team)
		linksused[link] = team

newlines = []

for team in linknames:
	line = []
	for name in linkdata[team]['names']:
		if name != team:
			line.append('["{}"] = "{}",'.format(name,team))
	print(linkdata[team])
	line.append('["{}"] = {{ link = "{}", long = "{}", medium = "{}", short = "{}" }},'.format(
		team,
		linkdata[team]['teamLink'],
		linkdata[team]['teamLong'],
		linkdata[team]['teamLong'],
		linkdata[team]['teamShort']
	))
	newlines.append('\n'.join(line))

output = '\n\n'.join(newlines)

with open('vg output.txt','w', encoding="utf-8") as f:
	f.write(output)