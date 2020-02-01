from cron_tasks import CronTasks
import match_schedule_hash as ms_hash
import predictions_verify as predictions
import patrol_namespaces as patrol

if __name__ == '__main__':
	tasks = CronTasks(
		interval=15,
		wikis=['lol', 'cod-esports']
	)
	tasks.run_revs(ms_hash.run, ['lol'])
	tasks.run_revs(predictions.run, ['lol'])
	tasks.run_revs(patrol.run, ['lol', 'cod-esports'])
