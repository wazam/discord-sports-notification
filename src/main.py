import discord
from discord.ext import tasks, commands
from os import getenv
from requests import get

CONFIG = {
    'pt_differential': 100,
    'mins_left': 4,
    'period': 4
}

notified_games = {}

bot = commands.Bot(command_prefix=">", description='{([<*_*>])} Alan is alive, but I can not tell u where he is')

@bot.event
async def on_ready():
	print(f'{bot.user.name} is online and ready!')
	notify_games.start()

@tasks.loop(seconds=5)
async def notify_games():
    channel = bot.get_channel(721483400560771182)
    games_to_notify = collect_games_to_notify()

    for game in games_to_notify:
        await channel.send(f'{game["home_text"]}-{game["away_text"]}-{game["time_left"]}')

def get_todays_nba_data():
    resp = get('https://data.nba.net/10s/prod/v2/today.json')
    data = resp.json()
    scoreboard_endpoint = data['links']['todayScoreboard']
    todays_games_resp = get("https://data.nba.net/10s" + scoreboard_endpoint)
    todays_games_data = todays_games_resp.json()
    return todays_games_data

def collect_games_to_notify():
    todays_games_data = get_todays_nba_data()
    todays_games = todays_games_data['games']

    games_to_notify = []

    for game in todays_games:

        home = game['hTeam']
        away = game['vTeam']

        if game['isGameActivated'] and game['period']['current'] >= CONFIG['period']:
            clock = game['clock'].split(':')
            
            if len(clock) < 2:
                minutes = 0
            else:
                minutes = int(clock[0])

            pts_difference = abs(int(home['score']) - int(away['score']))

            current_period = game['period']['current']
            period = ""
            if current_period > 4:
                period = (str(current_period % 4) + 'OT')
            else:
                period = str(current_period) + 'Q'

            if minutes <= CONFIG['mins_left'] and pts_difference <= CONFIG['pt_differential']:
                found_game = notified_games.get(game['gameId'])

                if found_game == None:
                    time_left = period + ' ' + game['clock']

                    home_text = home['triCode'] + ' ' + str(home['score'])
                    away_text = away['triCode'] + ' ' + str(away['score'])

                    notified_games[game['gameId']] = game['homeStartDate']
                    games_to_notify.append({ "home_text": home_text, "away_text": away_text, "time_left": time_left })
                else:
                    continue

    return games_to_notify

bot.run(getenv('DISCORD_SECRET_TOKEN'))