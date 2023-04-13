import discord
from discord.ext import tasks, commands
from os import environ
from datetime import date

from nba_games import NBAGamesChecker
from mlb_games import MLBGamesChecker

command_prefix = environ.get('BOT_PREFIX', "!")
description = '( ͡° ͜ʖ ͡°) Alan is alive, but I cannot tell you where he is.'
activity = discord.Activity(type=discord.ActivityType.watching, name=command_prefix + "help")
bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all(), description=description, activity=activity, status=discord.Status.online, case_insensitive=True)
refresh_rate = float(environ.get('BOT_REFRESH', 300))
NBA_enabled = eval(environ.get('NBA_ENABLED', True))
MLB_enabled = eval(environ.get('MLB_ENABLED', True))

nba_checker = NBAGamesChecker()
mlb_checker = MLBGamesChecker()

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online and ready!', flush=True)
    notify_all_games.start()

@bot.command()
async def ping(ctx):
    latency =  round(bot.latency * 1000)
    await ctx.send(f'Pong! `{latency}ms`')

@bot.command()
async def hello(ctx):
    msg = f'Hi {ctx.author.mention}'
    await ctx.send(msg)

@bot.command(aliases=['findalan'])
async def whereisalan(ctx):
    msg = f'{description}'
    await ctx.send(msg)

@bot.command()
async def passtheboof(ctx):
    msg = f':here:'
    await ctx.send(msg)

@bot.command(aliases=['petealonso'])
async def mets(ctx):
    msg = f'http://blabseal.org/coolbeans/'
    await ctx.send(msg)

@bot.command()
async def whoami(ctx):
    msg = f'https://github.com/wazam/discord-sports-notification'
    await ctx.send(msg)

@bot.command(aliases=['today'])
async def games(ctx):
    text = ""
    if NBA_enabled:
        num_nba_games = NBAGamesChecker().prefix_command_for_games()
        if num_nba_games > 0:
            text += str(num_nba_games)
        else:
            text += 'No'
        text += ' NBA game'
        if num_nba_games != 1:
            text += 's'
    if NBA_enabled and MLB_enabled:
        text += ' and '
    if MLB_enabled:
        todays_games_data = MLBGamesChecker().get_games()
        num_mlb_games = int(todays_games_data['totalGames'])
        if num_mlb_games > 0:
            text += str(num_mlb_games)
        else:
            text += 'No'
        text += ' MLB game'
        if num_mlb_games != 1:
            text += 's'
    if NBA_enabled or MLB_enabled:
        today = date.today().strftime("%b %-d, %Y")
        text += ' today, ' + str(today) + '.'
    msg = f'{text}'
    await ctx.send(msg)

@tasks.loop(seconds=refresh_rate)
async def notify_all_games():
    channel = bot.get_channel(int(environ.get('DISCORD_CHANNEL_ID')))
    if NBA_enabled:
        nba_games_to_notify = nba_checker.check_games()
        for game in nba_games_to_notify:
            await channel.send(f'{game["home_text"]} - {game["away_text"]} - {game["time_left"]}')
    if MLB_enabled:
        mlb_games_to_notify = mlb_checker.check_games()
        for game in mlb_games_to_notify:
            await channel.send(f'{game["home_text"]} - {game["away_text"]} - {game["time_left"]}')

bot.run(environ.get('DISCORD_SECRET_TOKEN'))
