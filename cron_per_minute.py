from log_into_wiki import login
import ro_news_webhook as ro_news
import move_blank_edit as move


if __name__ == '__main__':
	site = login('me', 'lol')
	logs = site.logs_by_interval(1)
	ro_news.run(logs)
	move.run(site, logs)
