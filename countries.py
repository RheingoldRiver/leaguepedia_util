with open('countries.txt') as f:
	tbl = f.readlines()

for i, line in enumerate(tbl):
	if line.strip().endswith(' -- REPLACE'):
		line = line.replace(' -- REPLACE', '')
		line = line.lower()
		tbl[i] = line

with open('countries.txt', 'w') as f:
	f.write(''.join(tbl))