from mwparserfromhell import parse
from mwparserfromhell.nodes import Template

text = '{{Test<!-- -->|param=value<!-- -->}}'

wikitext = parse(text)

for template in wikitext.filter_templates():
	print(template.name.strip())
	print(template.name.matches('Test'))
	template: Template
	for param in template.params:
		print(param.value.matches('value'))
