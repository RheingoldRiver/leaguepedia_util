import os
import re
d = "S:\Documents\Wikis\Random Temp\Folders\Imgur Album  JDG Spring Split 2020 Posters"

for file in os.listdir(d):
	orig = d + '\\' + file
	new = file.replace('DG', 'JDG')
	os.rename(orig, d + '\\' + new)