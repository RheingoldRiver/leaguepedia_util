from log_into_wiki import login
import ro_news_webhook as ro_news
import move_blank_edit as move


if __name__ == '__main__':
	site = login('me', 'lol')
	logs = site.logs_by_interval(1)
	try:
		ro_news.run(logs)
	except Exception as e:
		# TODO: Set up nice global error reporting method
		pass
	try:
		move.run(site, logs)
	except Exception as e:
		pass
