import discord
from discord.ext import tasks, commands
from os import getenv
from requests import get

from nba_games import NBAGamesChecker

bot = commands.Bot(command_prefix=">", description='{([<*_*>])} Alan is alive, but I can not tell u where he is')

nba_checker = NBAGamesChecker()

@bot.event
async def on_ready():
	print(f'{bot.user.name} is online and ready!')
	notify_games.start()

@tasks.loop(seconds=5)
async def notify_games():
    channel = bot.get_channel(721483400560771182)
    await nba_checker.notify_games(channel)

bot.run(getenv('DISCORD_SECRET_TOKEN'))