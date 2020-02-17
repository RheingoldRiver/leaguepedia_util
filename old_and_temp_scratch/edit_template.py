from log_into_wiki import *
import mwparserfromhell

class TemplateEditor(object):
	current_page = None # mwclient.Page object
	current_wikitext = None
	summary = 'Bot Edit' # Set summary
	page_list = []
	def __init__(self, site, limit = -1, startat_page = None):
		self.site = site
		self.limit = limit
		self.start_page = None
	
	def save_if_changed(self, newtext):
		if self.current_page.text() != newtext:
			print('Sa	ving page %s...' % self.current_page.name)
			self.current_page.save(newtext, summary=self.summary)
		else:
			print('Skipping page %s...' % self.current_page.name)
	
	def do_things(self, page_list_generator, startat_page = None):
		self.startat_page = None
		get_page_list(page_list_generator)
		passed_startat = False if self.startat_page else True
		lmt = 0
		for page in self.page_list:
			self.current_page = page
		if lmt == self.limit:
			break
		if startat_page and self.current_page.name == startat_page:
			passed_startat = True
		if not passed_startat:
			print("Skipping page %s" % self.current_page.name)
			continue
		lmt += 1
		self.process_page()
		self.save_if_changed(newtext)
	
	def process_page(self):
		self.current_wikitext = mwparserfromhell.parse(self.current_page.text())
		for template in self.current_wikitext.filter_templates():
			if tl_matches(template, ['TEMPLATEYOUCAREABOUT']):
				self.update_template(template)
	
class PageListGenerators(object):
	def via_transclusion(self, template):
		this_template = self.site.pages['Template:%s' % template]
		self.page_list = this_template.embeddedin()
	
	def via_file(self, file):
		with open('pages.txt', encoding="utf-8") as f:
			pages = [self.site.pages[_] for _ in f.readlines()]
	
class CurrentTemplateEditor(TemplateEditor, PagelistGenerators):
	def __init__(self):
		self.get_page_list = self.via_file
	
	def update_template(self, template):
		# TODO
