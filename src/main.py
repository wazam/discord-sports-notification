from discord.ext import tasks, commands
from os import environ

from nba_games import NBAGamesChecker
from mlb_games import MLBGamesChecker

bot = commands.Bot(command_prefix=">", description='{([<*_*>])} Alan is alive, but I can not tell u where he is')

nba_checker = NBAGamesChecker()
mlb_checker = MLBGamesChecker()

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online and ready!')
    notify_games.start()

@tasks.loop(seconds=10)
async def notify_games():
    channel = bot.get_channel(environ.get('DISCORD_CHANNEL_ID'))
    if eval(environ.get('NBA_ENABLED', True)) == True:
        await nba_checker.notify_games(channel)
    if eval(environ.get('MLB_ENABLED', False)) == True:
        await mlb_checker.notify_games(channel)

bot.run(environ.get('DISCORD_SECRET_TOKEN'))