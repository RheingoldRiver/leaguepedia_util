from cron_tasks import CronTasks
import ro_news_webhook as ro_news
import move_blank_edit as move

if __name__ == '__main__':
	tasks = CronTasks(
		interval=1,
		wikis=['lol', 'cod-esports']
	)
	tasks.run_logs(ro_news.run, ['lol'])
	tasks.run_logs(move.run, ['lol'])
