import requests
import re, json, urllib.request, urllib.error, math, copy

class WikiHelper:
    """
    Helper class to help querying pages and data in a wiki site
    """
    def getPagesByTemplate(self, site, template):
        this_template = site.pages[template] # Set template
        pages = this_template.embeddedin()
        return pages
