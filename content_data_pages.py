from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from datetime import date, timedelta
import mwparserfromhell

overview_text = '<includeonly>{{%s Navbox|year={{#titleparts:{{PAGENAME}}|1|2}}}}</includeonly><noinclude>{{documentation}}</noinclude>'

end_text = '<includeonly>{{#invoke:%s|endTable}}</includeonly><noinclude>{{documentation}}</noinclude>'

date_text = '<includeonly>{{#invoke:%s|date}}</includeonly><noinclude>{{documentation}}</noinclude>'

start_text = '<includeonly>{{#invoke:%s|start}}{{TOCFlat}}</includeonly><noinclude>{{documentation}}</noinclude>'

navbox_text = """{{Navbox
|name={{subst:PAGENAME}}
|title=%s Index
|image=
|state=mw-collapsible

|group1=Years
|list1={{Flatlist}}
{{Endflatlist}}
|group2={{{year|}}}
|list2={{Flatlist}}
{{#switch:{{{year|}}}
}}
{{Endflatlist}}

}}<noinclude>[[Category:Navboxes]]</noinclude>"""

site: EsportsClient = None

lookup = {
	"news" : { "template_prefix" : "NewsData",
			   "data_prefix" : "News",
			   "navbox_template" : "NewsData"
			   },
	"ec" : { "template_prefix" : "ExternalContent",
			 "data_prefix" : "ExternalContent",
			 "navbox_template" : "External Content"
			 },
	"rc" : {
		"template_prefix" : "RosterChangeData",
		"data_prefix" : "RosterChanges",
		"navbox_template" : "Roster Change Data"
	},
	"rumors" : {
		"template_prefix" : "RosterRumorData",
		"data_prefix" : "RosterRumors",
		"navbox_template" : "Roster Rumor Data"
	}
}

def allsundays(year):
	d = date(year, 1, 1)						  # January 1st
	d += timedelta(days = 6 - d.weekday())  # First Sunday
	while d.year == year:
		yield d
		d += timedelta(days = 7)

def make_data_pages(years, this, startat_page = None):
	passed_startat = True
	if startat_page:
		passed_startat = False
	template_prefix = lookup[this]["template_prefix"]
	data_prefix = lookup[this]["data_prefix"]
	navbox_template = lookup[this]["navbox_template"]
	summary = 'Initializing %s Pages' % template_prefix  # Set summary
	for year in years:
		site.client.pages['Data:{}/{}'.format(data_prefix, year)].save('{{%sOverview}}' % template_prefix, summary=summary)
		year_switch = '|' + str(year) + '='
		list_of_sundays = [year_switch]
		for d in allsundays(year):
			list_of_sundays.append('* [[Data:{}/{}|{}]]'.format(data_prefix, d.strftime('%Y-%m-%d'), str(d.strftime('%b %d'))))

			# START SAVING DATA PAGES - COMMENT THIS BLOCK TO DO NAVBOX ONLY
			page_prefix = 'Data:{}/'.format(data_prefix)
			page_name = page_prefix + str(d)
			if page_name == startat_page:
				passed_startat = True
			if not passed_startat:
				continue
			p = site.client.pages[page_name]
			redirect_text = '#redirect[[%s]]' % page_name
			check_and_make_redirects(d, page_prefix, redirect_text)
			if p.exists:
				continue
			lines = [ '{{%s/Start}}' % template_prefix ]
			weekday_index = d
			for i in range(0,7):
				y = weekday_index.year
				m = '{:02d}'.format(weekday_index.month)
				day = '{:02d}'.format(weekday_index.day)
				lines.append('== {} =='.format(weekday_index.strftime('%b %d')))
				lines.append('{{{{{}/Date|y={}|m={}|d={}}}}}'.format(template_prefix, y, m, day))
				weekday_index += timedelta(days = 1)
				lines.append('{{%s/End}}' % template_prefix)
			p.save('\n'.join(lines), summary=summary)
			# END SAVING DATA PAGES - COMMENT THIS BLOCK TO DO NAVBOX ONLY

		list_of_sundays.append('}}\n{{Endflatlist}}')
		template_page = site.client.pages['Template:%s Navbox' % navbox_template]
		wikitext = mwparserfromhell.parse(template_page.text())
		for template in wikitext.filter_templates():
			if template.name.matches('Navbox'):
				text = str(template.get('list1').value.strip())
				list_text = template.get('list2').value.strip()
				if year_switch in list_text:
					break
				text = text.replace('{{Endflatlist}}',
									'* [[Data:{}/{}|{}]]\n{{{{Endflatlist}}}}'.format(data_prefix, str(year), str(year)))
				template.add('list1', text)
				list_text = list_text.replace('}}\n{{Endflatlist}}', '\n'.join(list_of_sundays))
				template.add('list2', list_text)
		template_page.save(str(wikitext))

def make_templates(this):
	template_prefix = lookup[this]["template_prefix"]
	navbox_template = lookup[this]["navbox_template"]
	data_prefix = lookup[this]["data_prefix"]
	summary = 'Initializing %s Pages' % template_prefix  # Set summary
	site.client.pages['Template:%sOverview' % template_prefix].save(overview_text % navbox_template, summary=summary)
	site.client.pages['Template:%s/End' % template_prefix].save(end_text % template_prefix, summary=summary)
	site.client.pages['Template:%s/Date' % template_prefix].save(date_text % template_prefix, summary=summary)
	site.client.pages['Template:%s Navbox' % navbox_template].save(navbox_text % data_prefix, summary=summary)
	site.client.pages['Template:%s/Start' % template_prefix].save(start_text % template_prefix, summary=summary)

def check_and_make_redirects(d, page_prefix, redirect_text):
	weekday_index = d
	for i in range(0, 6):
		weekday_index += timedelta(days=1)
		y = weekday_index.year
		m = '{:02d}'.format(weekday_index.month)
		day = '{:02d}'.format(weekday_index.day)
		site.client.pages[page_prefix + '{}-{}-{}'.format(y, m, day)].save(redirect_text)


if __name__ == "__main__":
	this = 'news'
	site = EsportsClient('splatoon2-esports', user_file='bot')  # Set wiki
	make_templates(this)
	make_data_pages(range(20020,2021), this, startat_page=None)
