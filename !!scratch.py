import os

p = "S:\Documents\Wikis\Pronunciation\Danish_players\Kaelegrisen"

parent = os.path.normpath(p)

folders = []

for r, d, f in os.walk(parent):
	for folder in d:
		folders.append(os.path.join(parent, folder))

files = []
new_names = []

for folder in folders:
	for r, d, f in os.walk(folder):
		for file in f:
			if 'Danish' in file:
				files.append(os.path.join(folder, file))
				new_names.append(file)

for i, file in enumerate(files):
	os.rename(file, os.path.join(parent, new_names[i]))
