from log_into_wiki import login

def run(site, logs):
	for log in logs:
		print(log)
		if 'action' not in log.keys() or log['action'] != 'move':
			continue
		old_page_name = log['title']
		new_page_name = log['params']['target_title']
		if 'suppressredirect' not in log['params'].keys():
			site.pages[old_page_name].touch()
		new_page = site.pages[new_page_name]
		new_page.touch()
		new_page.touch()
		print(old_page_name)
		
	
if __name__ == '__main__':
	site = login('me', 'lol')
	run(site, site.logs_by_interval(40))
