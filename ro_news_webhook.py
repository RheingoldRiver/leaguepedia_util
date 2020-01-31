import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from log_into_wiki import *

site = login('bot', 'lol')

with open('webhook_leona.txt') as f:
	webhook_url = f.read().strip()

webhook = DiscordWebhook(url=webhook_url)

def run(logs):
	for log in logs['query']['logevents']:
		if type != 'ro-news':
			continue
		if 'custom-1' in log['params'].keys():
			send_event(log['params']['custom-1'], log['params']['custom-2'])

def send_event(text, team):
	embed = DiscordEmbed(
		title=team if team and team.strip() != "" else "News RefreshOverview",
		description=text
	)
	webhook.add_embed(embed)
	webhook.execute()

if __name__ == '__main__':
	site = login('me', 'lol')
	run(site.recentchanges_by_interval(1))
