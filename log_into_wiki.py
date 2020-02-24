import re, urllib.request, io
import extended_site
from esports_site import EsportsSite
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def log_into_fandom(user, wiki):
	if user == 'me':
		password = open('password_fandom.txt').read().strip()
		site = extended_site.ExtendedSite('%s.fandom.com' % wiki, path='/')
		site.login('RheingoldRiver', password)
		return site

def report_errors(report_page, page, errors):
	text = report_page.text()
	error_text = '\n* '.join([e.args[0] for e in errors])
	newtext = text + '\n==Python Error Report==\nPage: [[{}]] Messages:\n* {}'.format(page, error_text)
	report_page.save(newtext)
