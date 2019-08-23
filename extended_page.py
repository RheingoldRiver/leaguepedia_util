import mwclient.page

class ExtendedPage(mwclient.page.Page):
	def __init__(self, page):
		super().__init__(page.site, page.name, info=page._info)
		self.base_title = self.page_title.split('/')[0]
		self.base_name = self.name.split('/')[0]
	
	@staticmethod
	def extend_pages(page_gen):
		for page in page_gen:
			yield(ExtendedPage(page))
			
	def touch(self, check_existence=False):
		if check_existence and not self.exists:
			return
		self.site.api(
			'edit',
			title=self.name,
			appendtext="",
			token=self.get_token('edit'),
			summary="ExtendedPage Touch Edit"
		)
