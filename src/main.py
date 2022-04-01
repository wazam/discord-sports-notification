import discord
from discord.ext import tasks, commands
from os import getenv
from requests import get

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
    channel = bot.get_channel(getenv('DISCORD_CHANNEL_ID'))
    await nba_checker.notify_games(channel)
    await mlb_checker.notify_games(channel)

bot.run(getenv('DISCORD_SECRET_TOKEN'))